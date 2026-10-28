from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PATTERNS = (
    "0.075",
    "TYPE1_CALIBRATION_SCENARIO_MATRIX_V3",
    "TYPE1_CALIBRATION_SCENARIO_MATRIX_V4",
    "V3",
    "V4",
    "confirmatory_execution_authorized",
    "formal_calibration_pass",
)

def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], text=True, stderr=subprocess.STDOUT
    )

def classify(path: str, content: str, line: str) -> tuple[str, str]:
    lower_path = path.lower()
    lower_content = content.lower()

    if lower_path.startswith(".github/workflows/"):
        if (
            "exit 1" in lower_content
            and ("blocked" in lower_content or "not authorized" in lower_content)
        ):
            return (
                "WORKFLOW_CONTROL_PATH",
                "Workflow exists; inspect guard ordering and runner invocation",
            )
        if any(token in lower_content for token in (
            "calibrate_null_type1_scenario",
            "calibrate_null_type1.py",
            "type1_calibration_pilot",
        )):
            return (
                "EXECUTION_CAPABLE_WORKFLOW_CANDIDATE",
                "May invoke an execution path; inspect triggers and all guards",
            )
        return (
            "WORKFLOW_REFERENCE",
            "Workflow reference; execution capability not inferred from this line alone",
        )

    if lower_path.startswith("analysis/") or lower_path.startswith("scripts/"):
        return (
            "CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW",
            "Inspect entry points, callers, flags, and authorization guards",
        )

    if lower_path.startswith("tests/"):
        return (
            "TEST_OR_GUARD",
            "Diagnostic/test reference; not itself evidence of scientific approval",
        )

    if lower_path.startswith("protocol/") or lower_path.endswith((".md", ".json")):
        if "0.075" in line or "0.075" in lower_content:
            return (
                "POLICY_OR_HISTORICAL_REFERENCE",
                "Determine whether this is historical, diagnostic, or proposed policy",
            )
        return (
            "PROTOCOL_OR_DOCUMENTATION_REFERENCE",
            "Document reference; does not itself authorize execution",
        )

    return (
        "OTHER_REFERENCE",
        "Manual review required",
    )

def inspect_ref(ref: str) -> dict:
    commit = git("rev-parse", ref).strip()
    paths = git("ls-tree", "-r", "--name-only", ref).splitlines()
    entries = []

    for path in paths:
        try:
            content = git("show", f"{ref}:{path}")
        except subprocess.CalledProcessError:
            continue

        matching = []
        for number, line in enumerate(content.splitlines(), 1):
            if any(pattern.lower() in line.lower() for pattern in PATTERNS):
                kind, capability = classify(path, content, line)
                matching.append({
                    "line": number,
                    "text": line.strip(),
                    "classification": kind,
                    "execution_or_authority_review": capability,
                })

        if matching:
            entries.append({
                "path": path,
                "matches": matching,
                "workflow_dispatch_present": (
                    "workflow_dispatch:" in content
                    if path.startswith(".github/workflows/")
                    else None
                ),
                "runner_invocation_candidate": (
                    any(token in content for token in (
                        "calibrate_null_type1_scenario",
                        "calibrate_null_type1.py",
                        "type1_calibration_pilot",
                    ))
                    if path.startswith(".github/workflows/")
                    else None
                ),
            })

    return {
        "ref_requested": ref,
        "commit_sha": commit,
        "pattern_set": list(PATTERNS),
        "files_with_matches": len(entries),
        "entries": entries,
        "interpretation": (
            "Automated inventory for review, not an authorization decision. "
            "Workflow and code execution capability requires manual call-path review."
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
            f"{ref['files_with_matches']} files with matching references"
        )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
