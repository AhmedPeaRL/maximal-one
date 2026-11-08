from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# These are discovery tokens, not authorization decisions. Runner tokens are
# included so the actual invocation line becomes its own occurrence.
PATTERNS = (
    "0.075",
    "TYPE1_CALIBRATION_SCENARIO_MATRIX_V3",
    "TYPE1_CALIBRATION_SCENARIO_MATRIX_V4",
    "V3",
    "V4",
    "confirmatory_execution_authorized",
    "formal_calibration_pass",
    "promotion_authority",
    "claim_support",
    "freeze_state",
    "APPROVED_FROZEN",
    "archive_git_identity_verified",
    "not authorized",
    "BLOCKED",
    "exit 1",
    "calibrate_null_type1_scenario",
    "calibrate_null_type1.py",
    "type1_calibration_pilot",
)

# The tracked ledger is generated review evidence. Scanning its serialized
# rows as source creates recursive, self-amplifying occurrences. Keep it in
# the exact-review snapshot as a hash-only scope item, but exclude its contents
# from occurrence discovery. Any future generated evidence path must be added
# here explicitly and will be recorded in the inventory output.
EXCLUDED_GENERATED_PATHS = {
    "protocol/TYPE1_V3_V4_OCCURRENCE_LEVEL_MANUAL_LEDGER_2026-10-31.json": (
        "Generated occurrence ledger; scanning serialized rows recursively "
        "duplicates prior inventory occurrences and inflates the source scope."
    ),
    "protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md": (
        "Governance register documents the inventory and its own evidence; "
        "scanning it creates self-referential occurrences. Retain the exact "
        "file in snapshot and SHA-256 scope, but exclude its contents from "
        "occurrence discovery."
    ),
    "evidence/CURRENT_EVIDENCE_REGISTER.json": (
        "Generated snapshot-specific evidence register from an earlier audit; "
        "scanning it recursively counts stale run identities and prior inventory "
        "records as source occurrences. Retain it in the exact snapshot scope."
    ),
    "evidence/main_occurrence_level_manual_ledger.json": (
        "Generated occurrence ledger from an earlier audit; retain and hash it "
        "in the snapshot, but do not recursively scan its serialized rows."
    ),
    "evidence/occurrence_level_manual_ledger.json": (
        "Generated occurrence ledger from an earlier audit; retain and hash it "
        "in the snapshot, but do not recursively scan its serialized rows."
    ),
    "evidence/provenance.json": (
        "Generated provenance for an earlier inventory run; scanning it would "
        "count prior commit and workflow identities as source occurrences."
    ),
    "evidence/reference_inventory.json": (
        "Generated inventory from an earlier audit; scanning its serialized "
        "matches recursively duplicates old occurrences and inflates the scope."
    ),
    "evidence/snapshot_manifest.json": (
        "Generated snapshot manifest from an earlier audit; scanning its file "
        "paths, hashes, and policy fields creates recursive occurrences."
    ),
    "evidence/three_way_identity_certificate.json": (
        "Generated identity certificate from an earlier audit; retain it in the "
        "snapshot but exclude its prior run and commit identifiers from discovery."
    ),
    "adjudication/review_1711_e41fb_adjudication_template.csv": (
        "Generated adjudication template populated from an earlier inventory; "
        "its copied occurrence rows are review data, not primary source code."
    ),
    "adjudication/main_583_fe0d_adjudication_template.csv": (
        "Generated adjudication template populated from an earlier inventory; "
        "its copied occurrence rows are review data, not primary source code."
    ),
}

RUNNER_RE = re.compile(
    r"(?:python(?:3)?\s+)(?:-m\s+(?:analysis\.)?"
    r"(?:calibrate_null_type1(?:_scenario)?|type1_calibration_pilot)"
    r"|(?:analysis/)?(?:calibrate_null_type1(?:_scenario)?|"
    r"type1_calibration_pilot)\.py)",
    re.IGNORECASE,
)

CONTROL_RE = re.compile(
    r"confirmatory_execution_authorized|formal_calibration_pass|"
    r"promotion_authority|claim_support|freeze_state|APPROVED_FROZEN|"
    r"V4_APPROVED|archive_git_identity_verified|not authorized|"
    r"\bBLOCKED\b|\bexit\s+1\b",
    re.IGNORECASE,
)


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], text=True, stderr=subprocess.STDOUT
    )


def git_bytes(*args: str) -> bytes:
    """Read a Git blob as bytes so binary content cannot crash UTF-8 decoding."""
    return subprocess.check_output(
        ["git", *args], stderr=subprocess.STDOUT
    )


def _line_matches(line: str) -> bool:
    for pattern in PATTERNS:
        if pattern in {"V3", "V4"}:
            if re.search(rf"\b{pattern}\b", line, re.IGNORECASE):
                return True
        elif pattern.lower() in line.lower():
            return True
    return False


def classify(path: str, line: str) -> tuple[str, str]:
    """Classify this matched line only; never borrow evidence from other lines.

    This is an automated discovery label, not human adjudication. Full caller,
    guard-order, branch-trigger, and authorization review remains mandatory.
    """
    lower_path = path.lower()

    if lower_path.startswith(".github/workflows/"):
        if RUNNER_RE.search(line):
            return (
                "EXECUTION_CAPABLE_WORKFLOW_CANDIDATE",
                "This exact occurrence is a runner invocation; trace callers and guards.",
            )
        if CONTROL_RE.search(line):
            return (
                "WORKFLOW_CONTROL_PATH",
                "This exact occurrence names a guard or authority control; verify ordering.",
            )
        return (
            "WORKFLOW_REFERENCE",
            "This exact occurrence is a workflow reference, not a runner invocation by itself.",
        )

    if lower_path.startswith("analysis/") or lower_path.startswith("scripts/"):
        return (
            "CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW",
            "Inspect entry points, direct/indirect callers, flags, and authorization guards.",
        )

    if lower_path.startswith("tests/"):
        return (
            "TEST_OR_GUARD",
            "Test reference only; inspect what behavior is actually exercised.",
        )

    if lower_path.startswith("protocol/") or lower_path.endswith((".md", ".json")):
        if "0.075" in line:
            return (
                "POLICY_OR_HISTORICAL_REFERENCE",
                "Use the separate occurrence-local assessment to distinguish historical, diagnostic, or proposed context.",
            )
        if CONTROL_RE.search(line):
            return (
                "GOVERNANCE_REFERENCE",
                "Governance token on this exact line; not an execution authorization.",
            )
        return (
            "PROTOCOL_OR_DOCUMENTATION_REFERENCE",
            "Documentation reference; does not itself authorize execution.",
        )

    return "OTHER_REFERENCE", "Manual review required."


def _non_text_record(ref: str, path: str, raw: bytes) -> dict:
    """Record a binary/non-UTF-8 blob without treating it as adjudicated."""
    blob_object = git("rev-parse", f"{ref}:{path}").strip()
    return {
        "path": path,
        "reason": (
            "Git blob contains a NUL byte or is not valid UTF-8; it was not "
            "eligible for line-based text-token discovery."
        ),
        "handling": "EXCLUDED_FROM_OCCURRENCE_SCAN_RETAIN_IN_SNAPSHOT_SCOPE",
        "classification": "NON_TEXT_BLOB_NOT_LINE_SCANNED",
        "blob_object": blob_object,
        "size_bytes": len(raw),
        "content_sha256": hashlib.sha256(raw).hexdigest(),
    }


def inspect_ref(ref: str) -> dict:
    commit = git("rev-parse", ref).strip()
    paths = git("ls-tree", "-r", "--name-only", ref).splitlines()
    entries = []
    excluded_paths = []

    for path in paths:
        if path in EXCLUDED_GENERATED_PATHS:
            excluded_paths.append({
                "path": path,
                "reason": EXCLUDED_GENERATED_PATHS[path],
                "handling": "EXCLUDED_FROM_OCCURRENCE_SCAN_RETAIN_IN_SNAPSHOT_SCOPE",
            })
            continue

        try:
            raw = git_bytes("show", f"{ref}:{path}")
        except subprocess.CalledProcessError:
            continue

        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            excluded_paths.append(_non_text_record(ref, path, raw))
            continue

        # NUL bytes are a strong binary marker even when the byte sequence is
        # technically valid UTF-8. Preserve a hash-only record, not a text scan.
        if b"\x00" in raw:
            excluded_paths.append(_non_text_record(ref, path, raw))
            continue

        source_lines = content.splitlines()
        matching = []
        for number, line in enumerate(source_lines, 1):
            if not _line_matches(line):
                continue

            kind, capability = classify(path, line)
            context_start = max(1, number - 5)
            context_end = min(len(source_lines), number + 5)
            context_window = [
                {"line": context_line, "text": source_lines[context_line - 1]}
                for context_line in range(context_start, context_end + 1)
            ]
            matching.append({
                "line": number,
                "text": line.strip(),
                "classification": kind,
                "execution_or_authority_review": capability,
                "context_window": context_window,
            })

        if matching:
            workflow_runner_lines = [
                number for number, line in enumerate(source_lines, 1)
                if path.startswith(".github/workflows/") and RUNNER_RE.search(line)
            ]
            entries.append({
                "path": path,
                "matches": matching,
                "workflow_dispatch_present": (
                    "workflow_dispatch:" in content
                    if path.startswith(".github/workflows/") else None
                ),
                # File-level metadata only; never used to classify individual rows.
                "runner_invocation_candidate": bool(workflow_runner_lines)
                if path.startswith(".github/workflows/") else None,
                "runner_invocation_lines": workflow_runner_lines
                if path.startswith(".github/workflows/") else None,
            })

    return {
        "ref_requested": ref,
        "commit_sha": commit,
        "pattern_set": list(PATTERNS),
        "files_with_matches": len(entries),
        "entries": entries,
        "excluded_paths": excluded_paths,
        "interpretation": (
            "Occurrence labels are based on the exact matched line. Generated "
            "paths and non-text Git blobs are retained in the exact snapshot "
            "scope but excluded from line-based occurrence discovery. Generated "
            "evidence and adjudication templates are listed with explicit reasons; "
            "non-text exclusions include blob identity, byte size, and SHA-256. "
            "Inventory labels are not human adjudication or execution authority."
        ),
    }


def main() -> int:
    refs = sys.argv[1:] or ["HEAD"]
    report = {
        "audit": "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1",
        "refs": [inspect_ref(ref) for ref in refs],
    }
    out = Path("artifacts/type1_governance_inventory")
    out.mkdir(parents=True, exist_ok=True)
    destination = out / "reference_inventory.json"
    destination.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {destination}")
    for ref in report["refs"]:
        print(
            f"{ref['ref_requested']}: {ref['commit_sha']} — "
            f"{ref['files_with_matches']} files with matching references; "
            f"{len(ref['excluded_paths'])} paths excluded from occurrence scanning"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
