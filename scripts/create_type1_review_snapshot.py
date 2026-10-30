from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_BRANCH = "refs/heads/review/type1-v4-remediation"

REQUIRED_PATHS = [
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json",
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json",
    "protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md",
    "protocol/TYPE1_CALIBRATION_V4_ACCEPTANCE_RULE_DECISION_REQUEST.md",
    "protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json",
    "protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json",
    "protocol/TYPE1_V3_V4_GOVERNANCE_INVENTORY_2026-10-27.md",
    "protocol/TYPE1_V3_V4_MANUAL_CLASSIFICATION_LEDGER_2026-10-29.md",
    "protocol/TYPE1_ENGINEERING_EVIDENCE_ADDENDUM_2026-10-30.md",
    "protocol/TYPE1_REVIEW_SNAPSHOT_POLICY_V1.md",
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
    "requirements-lock.txt",
    "requirements.in",
    ".github/workflows/null-type1-calibration.yml",
    ".github/workflows/type1-calibration-runtime-pilot.yml",
    ".github/workflows/type1-full-path-equivalence.yml",
    ".github/workflows/type1-v3-v4-governance-audit.yml",
    ".github/workflows/type1-v4-assignment-matrix.yml",
    ".github/workflows/type1-v4-cli-resume-identity.yml",
    ".github/workflows/type1-v4-cross-runner-worker-order.yml",
    ".github/workflows/type1-v4-engineering-equivalence.yml",
    ".github/workflows/type1-review-snapshot.yml",
    "tests/test_type1_full_path_equivalence.py",
    "tests/test_type1_production_equivalence.py",
    "tests/test_type1_cli_resume_identity_rejections.py",
    "tests/test_type1_worker_assignment_matrix_invariance.py",
    "tests/test_type1_parallel_worker_order_equivalence.py",
    "tests/test_type1_cross_runner_workflow_branch_guard.py",
    "scripts/audit_type1_governance_refs.py",
    "scripts/create_type1_review_snapshot.py",
]


def git(*args: str) -> str:
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


def discover_scope() -> list[str]:
    tracked = git("ls-files", "-z").split("\0")
    selected = set(REQUIRED_PATHS)

    for item in tracked:
        if not item:
            continue

        path = Path(item)
        name = path.name.lower()

        if item.startswith("protocol/") and name.startswith("type1_"):
            selected.add(item)

        if item.startswith("analysis/") and (
            name.startswith("type1_")
            or name in {
                "appropriate_stochastic_null.py",
                "calibrate_null_type1.py",
                "calibrate_null_type1_scenario.py",
                "numerical_spectral_verification.py",
                "null_protocol.py",
            }
        ):
            selected.add(item)

        if item.startswith(".github/workflows/") and "type1" in name:
            selected.add(item)

        if item.startswith("tests/") and name.startswith("test_type1"):
            selected.add(item)

    return sorted(selected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--inventory-artifact-id", required=True)
    parser.add_argument("--inventory-source-commit", required=True)
    args = parser.parse_args()

    expected_commit = args.expected_commit.strip().lower()
    inventory_source_commit = (
        args.inventory_source_commit.strip().lower()
    )

    if len(expected_commit) != 40:
        raise SystemExit("BLOCKED: expected commit must be a full 40-char SHA")

    if inventory_source_commit != expected_commit:
        raise SystemExit(
            "BLOCKED: inventory source commit differs from review commit"
        )

    github_ref = os.environ.get("GITHUB_REF", "")
    if github_ref != EXPECTED_BRANCH:
        raise SystemExit(
            f"BLOCKED: expected {EXPECTED_BRANCH}; got {github_ref!r}"
        )

    actual_commit = git("rev-parse", "HEAD").lower()
    if actual_commit != expected_commit:
        raise SystemExit(
            "BLOCKED: checked-out commit mismatch: "
            f"{actual_commit} != {expected_commit}"
        )

    root = Path(".").resolve()
    output = root / "artifacts/type1_review_snapshot"
    output.mkdir(parents=True, exist_ok=True)

    scope = discover_scope()
    missing_required = [
        item for item in REQUIRED_PATHS
        if not (root / item).is_file()
    ]

    records = []
    for relative in scope:
        path = root / relative
        if not path.is_file():
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

    missing_scope = [
        row["path"] for row in records
        if row["status"] == "MISSING"
    ]

    manifest = {
        "schema": "HCM_TYPE1_REVIEW_SNAPSHOT_V2",
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "repository": "AhmedPeaRL/maximal-one",
        "review_ref": github_ref,
        "review_commit_sha": actual_commit,
        "inventory_artifact_id": args.inventory_artifact_id,
        "inventory_source_commit": inventory_source_commit,
        "scope_discovery": (
            "tracked Git files selected by explicit Type-I path rules"
        ),
        "required_path_count": len(REQUIRED_PATHS),
        "discovered_scope_count": len(scope),
        "present_file_count": sum(
            row["status"] == "PRESENT" for row in records
        ),
        "missing_required_paths": missing_required,
        "missing_scope_paths": missing_scope,
        "files": records,
        "protocol_freeze": "NOT_FROZEN",
        "formal_calibration_authorized": False,
        "claim_support": False,
        "promotion_authority": False,
    }

    manifest_path = output / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
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
        "commit": actual_commit,
        "inventory_artifact_id": args.inventory_artifact_id,
        "present": manifest["present_file_count"],
        "missing_required": missing_required,
        "missing_scope": missing_scope,
        "manifest": str(manifest_path),
        "sha256sums": str(sums_path),
    }, indent=2))

    if missing_required or missing_scope:
        print(
            "SNAPSHOT INCOMPLETE: missing files require reconciliation.",
            file=sys.stderr,
        )
        return 2

    print("SNAPSHOT HASHING COMPLETE.")
    print("No protocol freeze or formal authorization is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
