from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from scripts.generate_type1_occurrence_ledger import (
    occurrence_id as canonical_occurrence_id,
)

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

def inventory_scanner_exclusions(data: dict, expected_commit: str) -> list[dict]:
    refs = data.get("refs")
    if not isinstance(refs, list):
        raise SystemExit("BLOCKED: inventory refs must be a list.")
    matches = [
        row for row in refs
        if isinstance(row, dict)
        and row.get("commit_sha", "").lower() == expected_commit.lower()
    ]
    if len(matches) != 1:
        raise SystemExit("BLOCKED: cannot resolve exact inventory ref for exclusions.")
    raw = matches[0].get("excluded_paths", [])
    if not isinstance(raw, list):
        raise SystemExit("BLOCKED: inventory excluded_paths must be a list.")
    normalized = []
    seen = set()
    for item in raw:
        if not isinstance(item, dict):
            raise SystemExit("BLOCKED: malformed scanner exclusion record.")
        rel = safe_repo_path(item.get("path", ""))
        reason = item.get("reason")
        handling = item.get("handling")
        if not isinstance(reason, str) or not reason.strip():
            raise SystemExit(f"BLOCKED: exclusion reason missing for {rel}.")
        if not isinstance(handling, str) or not handling.strip():
            raise SystemExit(f"BLOCKED: exclusion handling missing for {rel}.")
        if rel in seen:
            raise SystemExit(f"BLOCKED: duplicate scanner exclusion: {rel}")
        seen.add(rel)
        normalized.append({"path": rel, "reason": reason, "handling": handling})
    return sorted(normalized, key=lambda row: row["path"])

def load_inventory(
    path: Path,
    expected_commit: str,
) -> tuple[dict, list[str], list[dict], str]:
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
    return data, sorted(paths), occurrences, ref_record["ref_requested"]

def select_snapshot_paths(
    inventory_paths: list[str],
    required_paths: list[str],
    scanner_exclusions: list[dict],
) -> list[str]:
    """Keep scanner-excluded evidence in the snapshot/hash scope."""
    return sorted(
        set(inventory_paths)
        | set(required_paths)
        | {row["path"] for row in scanner_exclusions}
    )


def build_snapshot_occurrence_rows(
    occurrences: list[dict],
    inventory_ref: str,
) -> list[dict]:
    rows = []
    seen = set()

    for occ in occurrences:
        oid = canonical_occurrence_id(
            inventory_ref,
            occ["path"],
            occ["line"],
            occ["match_index_within_file"],
        )

        if oid in seen:
            raise ValueError(
                f"Duplicate snapshot occurrence ID: {oid}"
            )

        seen.add(oid)

        rows.append({
            "occurrence_id": oid,
            **occ,
            "manual_classification": "UNKNOWN",
            "status": "OPEN",
        })

    return rows

def create_self_contained_archive(
    repo_root: Path,
    selected_paths: list[str],
    inventory_path: Path,
    ledger_path: Path,
    overlay_path: Path,
    output_dir: Path,
) -> tuple[Path, dict]:

    repo_root = repo_root.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    staging = output_dir / "staging"

    if staging.exists():
        shutil.rmtree(staging)

    source_repo = staging / "source/repository"
    source_evidence = staging / "source/evidence"

    source_repo.mkdir(parents=True)
    source_evidence.mkdir(parents=True)

    copied = []

    for rel in sorted(set(selected_paths)):
        safe = safe_repo_path(rel)
        source = (repo_root / safe).resolve()

        if not source.is_relative_to(repo_root):
            raise ValueError(
                f"Path escapes repository: {rel}"
            )

        if not source.is_file():
            raise FileNotFoundError(rel)

        target = source_repo / safe
        target.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source, target)

        copied.append(
            f"source/repository/{safe}"
        )

    evidence_inputs = {
        "reference_inventory.json": inventory_path,
        "occurrence_level_manual_ledger.json": ledger_path,
        "manual_adjudication_overlay.json": overlay_path,
    }

    for name, source in evidence_inputs.items():
        source = Path(source)

        if not source.is_file():
            raise FileNotFoundError(
                f"Missing evidence file: {source}"
            )

        target = source_evidence / name
        shutil.copy2(source, target)

        copied.append(
            f"source/evidence/{name}"
        )

    file_records = []

    for rel in sorted(copied):
        path = staging / rel

        file_records.append({
            "path": rel,
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })

    sums = "".join(
        f"{row['sha256']}  {row['path']}\n"
        for row in file_records
    )

    (staging / "SHA256SUMS.txt").write_text(
        sums,
        encoding="utf-8",
    )

    manifest = {
        "schema": "HCM_TYPE1_SELF_CONTAINED_REVIEW_SNAPSHOT_V1",
        "files": file_records,
        "file_count": len(file_records),
        "source_files_included": True,
        "hashes_calculated_from_copied_files": True,
        "archive_extraction_verification_required": True,
    }

    (staging / "manifest.json").write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    archive = output_dir / "self-contained-review-snapshot.zip"

    if archive.exists():
        archive.unlink()

    with zipfile.ZipFile(
        archive,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as z:
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                z.write(
                    path,
                    path.relative_to(staging).as_posix(),
                )

    verification = {
        "archive": archive.name,
        "verified": True,
        "checked_file_count": 0,
        "errors": [],
    }

    with zipfile.ZipFile(archive, "r") as z:
        names = set(z.namelist())

        for row in file_records:
            rel = row["path"]

            if rel not in names:
                verification["errors"].append(
                    f"MISSING:{rel}"
                )
                continue

            data = z.read(rel)
            digest = hashlib.sha256(data).hexdigest()

            if digest != row["sha256"]:
                verification["errors"].append(
                    f"HASH_MISMATCH:{rel}"
                )
                continue

            if len(data) != row["size_bytes"]:
                verification["errors"].append(
                    f"SIZE_MISMATCH:{rel}"
                )
                continue

            verification["checked_file_count"] += 1

    verification["verified"] = not verification["errors"]

    if not verification["verified"]:
        raise ValueError(
            "Self-contained snapshot verification failed: "
            + "; ".join(verification["errors"])
        )

    (staging / "verification").mkdir(
        parents=True,
        exist_ok=True,
    )

    (staging / "verification/extraction_verification.json").write_text(
        json.dumps(
            verification,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    return archive, verification

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--inventory-artifact-id", required=True)
    parser.add_argument("--inventory-source-commit", required=True)
    parser.add_argument("--inventory-json", required=True)
    parser.add_argument("--inventory-sha256", required=True)
    parser.add_argument("--ledger-json", required=True)
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
    inventory, inventory_paths, occurrences, inventory_ref = load_inventory(
        inventory_path,
        expected,
    )
    scanner_exclusions = inventory_scanner_exclusions(inventory, expected)

    root = Path(".").resolve()
    required_missing = [p for p in REQUIRED_PATHS if not (root / p).is_file()]
    # Dynamic scope is the union of every path in the exact-commit inventory
    # and the explicitly declared mandatory anchor paths.
    # Excluded generated evidence is not scanned for occurrences, but remains
    # in the exact snapshot's hash scope so the exclusion is auditable.
    selected = select_snapshot_paths(
        inventory_paths,
        REQUIRED_PATHS,
        scanner_exclusions,
    )
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
    inventory_occurrence_rows = build_snapshot_occurrence_rows(
        occurrences,
        inventory_ref,
    )

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
        "inventory_ref": inventory_ref,
        "scope_discovery": (
            "all matched paths in the exact-commit inventory, union explicit "
            "mandatory anchors and hash-only scanner-excluded generated evidence"
        ),
        "inventory_path_count": len(inventory_paths_set),
        "required_anchor_count": len(REQUIRED_PATHS),
        "selected_scope_count": len(selected),
        "present_file_count": sum(r["status"] == "PRESENT" for r in records),
        "missing_required_paths": required_missing,
        "missing_scope_paths": missing_scope,
        "excluded_paths": [],
        "scanner_exclusions": scanner_exclusions,
        "scanner_exclusion_count": len(scanner_exclusions),
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
    ledger_path = Path(args.ledger_json)
    overlay_path = out / "manual_adjudication_overlay.json"
    overlay_seed = {
        "schema": "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V1",
        "review_commit_sha": actual,
        "inventory_ref": inventory_ref,
        "inventory_sha256": actual_inventory_hash,
        "records": [],
    }
    overlay_path.write_text(
        json.dumps(overlay_seed, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    package_dir = out / "self_contained"
    archive, verification = create_self_contained_archive(
        repo_root=root,
        selected_paths=selected,
        inventory_path=inventory_path,
        ledger_path=ledger_path,
        overlay_path=overlay_path,
        output_dir=package_dir,
    )

    # Keep the extraction verification as a separate artifact file.
    verification_source = (
        package_dir / "staging" / "verification"
        / "extraction_verification.json"
    )
    verification_target = package_dir / "extraction_verification.json"

    shutil.copy2(verification_source, verification_target)

    # Avoid uploading a second, unpacked copy of all source files.
    shutil.rmtree(package_dir / "staging")

    if not verification.get("verified"):
        raise SystemExit("BLOCKED: self-contained archive verification failed.")

    print(json.dumps({
        "commit": actual,
        "inventory_artifact_id": args.inventory_artifact_id,
        "inventory_paths": len(inventory_paths),
        "selected_scope": len(selected),
        "occurrences": len(occurrences),
        "missing_required": required_missing,
        "missing_scope": missing_scope,
        "excluded_paths": [],
        "self_contained_archive": str(archive),
        "verified": verification["verified"],
        "checked_file_count": verification["checked_file_count"],
        "verification_file": str(verification_target),
    }, indent=2))
    if required_missing or missing_scope:
        print("SNAPSHOT INCOMPLETE: missing paths require explicit reconciliation.", file=sys.stderr)
        return 2
    print("DYNAMIC SNAPSHOT COMPLETE; no protocol or execution authority implied.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
