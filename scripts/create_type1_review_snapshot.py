from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

EXPECTED_BRANCH = "refs/heads/review/type1-v4-remediation"

# These are mandatory anchors, not the complete review scope.
REQUIRED_PATHS = ['protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json',
 'protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json',
 'protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md',
 'protocol/TYPE1_CALIBRATION_V4_ACCEPTANCE_RULE_DECISION_REQUEST.md',
 'protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json',
 'protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json',
 'protocol/TYPE1_V3_V4_GOVERNANCE_INVENTORY_2026-10-27.md',
 'protocol/TYPE1_V3_V4_MANUAL_CLASSIFICATION_LEDGER_2026-10-29.md',
 'protocol/TYPE1_ENGINEERING_EVIDENCE_ADDENDUM_2026-10-30.md',
 'protocol/TYPE1_REVIEW_SNAPSHOT_POLICY_V1.md',
 'analysis/calibrate_null_type1.py',
 'analysis/calibrate_null_type1_scenario.py',
 'analysis/appropriate_stochastic_null.py',
 'analysis/numerical_spectral_verification.py',
 'analysis/null_protocol.py',
 'analysis/type1_calibration_pilot.py',
 'analysis/type1_execution_artifacts.py',
 'analysis/merge_type1_execution_shards.py',
 'analysis/merge_type1_calibration_pilot_shards.py',
 'analysis/compare_type1_cross_runner.py',
 'analysis/type1_acceptance_operating_characteristics.py',
 'requirements-lock.txt',
 'requirements.in',
 '.github/workflows/null-type1-calibration.yml',
 '.github/workflows/type1-calibration-runtime-pilot.yml',
 '.github/workflows/type1-full-path-equivalence.yml',
 '.github/workflows/type1-v3-v4-governance-audit.yml',
 '.github/workflows/type1-v4-assignment-matrix.yml',
 '.github/workflows/type1-v4-cli-resume-identity.yml',
 '.github/workflows/type1-v4-cross-runner-worker-order.yml',
 '.github/workflows/type1-v4-engineering-equivalence.yml',
 '.github/workflows/type1-review-snapshot.yml',
 'tests/test_type1_full_path_equivalence.py',
 'tests/test_type1_production_equivalence.py',
 'tests/test_type1_cli_resume_identity_rejections.py',
 'tests/test_type1_worker_assignment_matrix_invariance.py',
 'tests/test_type1_parallel_worker_order_equivalence.py',
 'tests/test_type1_cross_runner_workflow_branch_guard.py',
 'scripts/audit_type1_governance_refs.py',
 'scripts/create_type1_review_snapshot.py']

def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], text=True, stderr=subprocess.STDOUT
    ).strip()

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def safe_repo_path(value: str) -> str:
    # Inventory paths are untrusted data. Reject absolute paths and traversal.
    p = PurePosixPath(value)
    if not value or p.is_absolute() or ".." in p.parts or "\\" in value:
        raise SystemExit(f"BLOCKED: unsafe inventory path: {value!r}")
    normalized = p.as_posix()
    if normalized.startswith(".git/") or normalized == ".git":
        raise SystemExit(f"BLOCKED: Git metadata path is not review content: {value!r}")
    return normalized

def load_inventory(path: Path, expected_commit: str) -> tuple[dict, list[str], list[dict]]:
    if not path.is_file():
        raise SystemExit(f"BLOCKED: inventory JSON not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("audit") != "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1":
        raise SystemExit("BLOCKED: unexpected governance inventory schema.")
    refs = data.get("refs")
    if not isinstance(refs, list):
        raise SystemExit("BLOCKED: inventory refs must be a list.")
    matches = [r for r in refs if r.get("commit_sha", "").lower() == expected_commit]
    if len(matches) != 1:
        raise SystemExit(
            "BLOCKED: inventory must contain exactly one ref for the expected commit; "
            f"found {len(matches)}."
        )
    ref_record = matches[0]
    entries = ref_record.get("entries")
    if not isinstance(entries, list):
        raise SystemExit("BLOCKED: inventory entries must be a list.")
    paths = set()
    occurrences = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise SystemExit("BLOCKED: malformed inventory entry.")
        rel = safe_repo_path(entry["path"])
        paths.add(rel)
        found = entry.get("matches", [])
        if not isinstance(found, list):
            raise SystemExit(f"BLOCKED: malformed matches for {rel}")
        for index, match in enumerate(found, 1):
            if not isinstance(match, dict):
                raise SystemExit(f"BLOCKED: malformed occurrence in {rel}")
            line = match.get("line")
            if not isinstance(line, int) or line < 1:
                raise SystemExit(f"BLOCKED: invalid line number in {rel}")
            text = match.get("text")
            if not isinstance(text, str):
                raise SystemExit(f"BLOCKED: invalid matched text in {rel}:{line}")
            occurrences.append({
                "path": rel,
                "line": line,
                "match_index_within_file": index,
                "text": text,
                "automated_classification": match.get("classification", "UNKNOWN"),
                "automated_note": match.get("execution_or_authority_review", ""),
            })
    if not paths:
        raise SystemExit("BLOCKED: inventory contains no matching paths.")
    return data, sorted(paths), occurrences

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--inventory-artifact-id", required=True)
    parser.add_argument("--inventory-source-commit", required=True)
    parser.add_argument("--inventory-json", required=True)
    parser.add_argument("--inventory-sha256", required=True)
    args = parser.parse_args()

    expected = args.expected_commit.strip().lower()
    source_commit = args.inventory_source_commit.strip().lower()
    if len(expected) != 40 or source_commit != expected:
        raise SystemExit("BLOCKED: inventory and snapshot commit identities differ.")
    if not args.inventory_artifact_id.isdigit():
        raise SystemExit("BLOCKED: inventory artifact ID must be numeric.")
    github_ref = os.environ.get("GITHUB_REF", "")
    if github_ref != EXPECTED_BRANCH:
        raise SystemExit(f"BLOCKED: expected {EXPECTED_BRANCH}; got {github_ref!r}")
    actual = git("rev-parse", "HEAD").lower()
    if actual != expected:
        raise SystemExit(f"BLOCKED: checked-out commit mismatch: {actual} != {expected}")

    inventory_path = Path(args.inventory_json)
    actual_inventory_hash = sha256_file(inventory_path)
    if actual_inventory_hash.lower() != args.inventory_sha256.strip().lower():
        raise SystemExit("BLOCKED: downloaded inventory JSON SHA-256 mismatch.")
    inventory, inventory_paths, occurrences = load_inventory(inventory_path, expected)

    root = Path(".").resolve()
    required_missing = [p for p in REQUIRED_PATHS if not (root / p).is_file()]
    # Dynamic scope is the union of every path in the exact-commit inventory
    # and the explicitly declared mandatory anchor paths.
    selected = sorted(set(inventory_paths) | set(REQUIRED_PATHS))
    records = []
    for rel in selected:
        path = root / rel
        if not path.is_file():
            records.append({"path": rel, "status": "MISSING", "sha256": None})
        else:
            records.append({
                "path": rel, "status": "PRESENT",
                "sha256": sha256_file(path), "size_bytes": path.stat().st_size,
            })

    missing_scope = [r["path"] for r in records if r["status"] == "MISSING"]
    inventory_paths_set = set(inventory_paths)
    inventory_occurrence_rows = []
    for occ in occurrences:
        rel = occ["path"]
        path_hash = hashlib.sha256(rel.encode("utf-8")).hexdigest()[:12]
        occurrence_id = (
            f"REVIEW/{path_hash}/{occ['line']}/"
            f"{occ['match_index_within_file']}"
        )
        inventory_occurrence_rows.append({
            "occurrence_id": occurrence_id,
            **occ,
            "manual_classification": "UNKNOWN",
            "status": "OPEN",
        })

    # Explicit exclusions: none are silently applied. Every inventory path is
    # included; unsafe paths block the run rather than being skipped.
    manifest = {
        "schema": "HCM_TYPE1_REVIEW_SNAPSHOT_V3",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": "AhmedPeaRL/maximal-one",
        "review_ref": github_ref,
        "review_commit_sha": actual,
        "inventory_artifact_id": args.inventory_artifact_id,
        "inventory_source_commit": source_commit,
        "inventory_json_sha256": actual_inventory_hash,
        "inventory_schema": inventory.get("audit"),
        "inventory_ref": next(
            r.get("ref_requested") for r in inventory["refs"]
            if r.get("commit_sha", "").lower() == expected
        ),
        "scope_discovery": (
            "all paths in the exact-commit governance inventory, union "
            "explicit mandatory anchors; no silent exclusions"
        ),
        "inventory_path_count": len(inventory_paths_set),
        "required_anchor_count": len(REQUIRED_PATHS),
        "selected_scope_count": len(selected),
        "present_file_count": sum(r["status"] == "PRESENT" for r in records),
        "missing_required_paths": required_missing,
        "missing_scope_paths": missing_scope,
        "excluded_paths": [],
        "files": records,
        "inventory_occurrences": inventory_occurrence_rows,
        "protocol_freeze": "NOT_FROZEN",
        "formal_calibration_authorized": False,
        "confirmatory_execution_authorized": False,
        "claim_support": False,
        "promotion_authority": False,
    }
    out = root / "artifacts/type1_review_snapshot"
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    sums = [f"{r['sha256']}  {r['path']}" for r in records if r["status"] == "PRESENT"]
    (out / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(json.dumps({
        "commit": actual,
        "inventory_artifact_id": args.inventory_artifact_id,
        "inventory_paths": len(inventory_paths),
        "selected_scope": len(selected),
        "occurrences": len(occurrences),
        "missing_required": required_missing,
        "missing_scope": missing_scope,
        "excluded_paths": [],
    }, indent=2))
    if required_missing or missing_scope:
        print("SNAPSHOT INCOMPLETE: missing paths require explicit reconciliation.", file=sys.stderr)
        return 2
    print("DYNAMIC SNAPSHOT COMPLETE; no protocol or execution authority implied.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
