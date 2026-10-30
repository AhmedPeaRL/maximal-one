from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BRANCH = "review/type1-v4-remediation"

FILES = [
    # Protocol and governance
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json",
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json",
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json",
    "protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md",
    "protocol/TYPE1_CALIBRATION_V4_ACCEPTANCE_RULE_DECISION_REQUEST.md",
    "protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json",
    "protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json",
    "protocol/TYPE1_V3_V4_GOVERNANCE_INVENTORY_2026-10-27.md",
    "protocol/TYPE1_V3_V4_MANUAL_CLASSIFICATION_LEDGER_2026-10-29.md",
    "protocol/TYPE1_ENGINEERING_EVIDENCE_ADDENDUM_2026-10-30.md",
    "protocol/TYPE1_REVIEW_SNAPSHOT_POLICY_V1.md",

    # Statistical implementation
    "analysis/calibrate_null_type1.py",
    "analysis/calibrate_null_type1_scenario.py",
    "analysis/appropriate_stochastic_null.py",
    "analysis/numerical_spectral_verification.py",
    "analysis/null_protocol.py",
    "analysis/type1_calibration_pilot.py",
    "analysis/type1_execution_artifacts.py",
    "analysis/merge_type1_execution_shards.py",
    "analysis/merge_type1_calibration_pilot_shards.py",
    "analysis/compare_type1_cross_runner.py",
    "analysis/type1_acceptance_operating_characteristics.py",

    # Dependencies
    "requirements-lock.txt",
    "requirements.in",

    # Workflows
    ".github/workflows/null-type1-calibration.yml",
    ".github/workflows/scientific-claim-promotion.yml",
    ".github/workflows/scientific-validation.yml",
    ".github/workflows/confirmatory-readiness-gate.yml",
    ".github/workflows/type1-calibration-runtime-pilot.yml",
    ".github/workflows/type1-full-path-equivalence.yml",
    ".github/workflows/type1-v3-v4-governance-audit.yml",
    ".github/workflows/type1-v4-engineering-equivalence.yml",
    ".github/workflows/type1-v4-cli-resume-identity.yml",
    ".github/workflows/type1-v4-assignment-matrix.yml",
    ".github/workflows/type1-v4-cross-runner-worker-order.yml",
    ".github/workflows/type1-review-snapshot.yml",

    # Tests
    "tests/test_v3_v4_governance_separation.py",
    "tests/test_type1_full_path_equivalence.py",
    "tests/test_type1_production_equivalence.py",
    "tests/test_type1_resume_cli_identity_rejections.py",
    "tests/test_type1_worker_assignment_matrix_invariance.py",
    "tests/test_type1_parallel_worker_order_equivalence.py",

    # Snapshot generator itself
    "scripts/create_type1_review_snapshot.py",
]


def git_text(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    args = parser.parse_args()

    branch = git_text("branch", "--show-current")
    commit = git_text("rev-parse", "HEAD")

    if branch != BRANCH:
        raise SystemExit(
            f"BLOCKED: expected branch {BRANCH}; found {branch}"
        )

    if commit != args.expected_commit:
        raise SystemExit(
            "BLOCKED: checked-out commit differs from requested "
            f"review commit: {commit}"
        )

    root = Path(".").resolve()
    output = root / "artifacts/type1_review_snapshot"
    output.mkdir(parents=True, exist_ok=True)

    records = []
    missing = []

    for relative in FILES:
        path = root / relative

        if not path.is_file():
            missing.append(relative)
            records.append({
                "path": relative,
                "status": "MISSING",
                "sha256": None,
            })
            continue

        records.append({
            "path": relative,
            "status": "PRESENT",
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })

    manifest = {
        "schema": "HCM_TYPE1_REVIEW_SNAPSHOT_V1",
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "repository": "AhmedPeaRL/maximal-one",
        "branch": branch,
        "commit_sha": commit,
        "expected_commit_sha": args.expected_commit,
        "file_count_declared": len(FILES),
        "file_count_present": sum(
            row["status"] == "PRESENT" for row in records
        ),
        "file_count_missing": len(missing),
        "missing_files": missing,
        "files": records,
        "protocol_freeze": "NOT_FROZEN",
        "formal_calibration_authorized": False,
        "claim_support": False,
        "promotion_authority": False,
    }

    manifest_path = output / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    sums_path = output / "SHA256SUMS.txt"
    sums = [
        f"{row['sha256']}  {row['path']}"
        for row in records
        if row["status"] == "PRESENT"
    ]
    sums_path.write_text(
        "\n".join(sums) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "commit_sha": commit,
        "present": manifest["file_count_present"],
        "missing": missing,
        "manifest": str(manifest_path),
        "sha256sums": str(sums_path),
    }, indent=2))

    if missing:
        print(
            "SNAPSHOT INCOMPLETE: one or more declared files are missing.",
            file=sys.stderr,
        )
        return 2

    print("SNAPSHOT FILE HASHING COMPLETE.")
    print("This does not freeze or authorize the scientific protocol.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
