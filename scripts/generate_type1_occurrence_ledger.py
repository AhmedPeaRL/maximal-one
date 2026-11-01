from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from scripts.type1_occurrence_classifier import classify_occurrence

INVENTORY_SCHEMA = "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1"
LEDGER_SCHEMA = "HCM_TYPE1_OCCURRENCE_MANUAL_LEDGER_V1"
RECONCILIATION_SCHEMA = "HCM_TYPE1_OCCURRENCE_LEDGER_RECONCILIATION_V1"

# These fields are intentionally initialized as unresolved. The generator must
# never infer a human classification, close an occurrence, or grant authority.
INITIAL_FIELDS: dict[str, Any] = {
    "manual_classification": "UNKNOWN",
    "historical_diagnostic_proposed_governance_status": "UNDETERMINED",
    "can_influence_execution": "UNKNOWN",
    "direct_caller_or_workflow_step": "OPEN",
    "indirect_call_path": "OPEN",
    "runner_entry_point_or_command": "OPEN",
    "trigger_conditions_and_branch_restrictions": "OPEN",
    "matrix_and_protocol_consumed": "OPEN",
    "authorization_guard_and_execution_order": "OPEN",
    "guard_fails_closed": "UNKNOWN",
    "negative_test": "NOT_YET_IDENTIFIED",
    "test_run_job_artifact_commit": "OPEN",
    "reviewer_disposition": "PENDING",
    "status": "OPEN",
    "closure_evidence": None,
    "unresolved_reason": (
        "Manual inspection required; automated classification is not final."
    ),
}


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def occurrence_id(ref_name: str, path: str, line: int, match_index: int) -> str:
    path_digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]
    return f"{ref_name}/{path_digest}/{line}/{match_index}"


def _validate_inventory(data: dict, expected_commit: str) -> dict:
    if not isinstance(data, dict) or data.get("audit") != INVENTORY_SCHEMA:
        raise ValueError("Unsupported governance inventory schema")

    refs = data.get("refs")
    if not isinstance(refs, list):
        raise ValueError("Inventory refs must be a list")

    matches = [
        ref for ref in refs
        if isinstance(ref, dict)
        and ref.get("commit_sha", "").lower() == expected_commit.lower()
    ]
    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one inventory ref matching the requested commit; "
            f"found {len(matches)}"
        )

    ref = matches[0]
    ref_name = ref.get("ref_requested")
    if not isinstance(ref_name, str) or not ref_name.strip():
        raise ValueError("Inventory ref_requested is missing")

    entries = ref.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Inventory entries must be a list")

    seen_occurrences: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Inventory entry must be an object")
        path = entry.get("path")
        matches_for_path = entry.get("matches")
        if not isinstance(path, str) or not path or path.startswith("/"):
            raise ValueError(f"Unsafe or missing repository path: {path!r}")
        if ".." in Path(path).parts or "\\" in path:
            raise ValueError(f"Unsafe repository path: {path!r}")
        if not isinstance(matches_for_path, list):
            raise ValueError(f"Matches must be a list for {path}")
        for index, match in enumerate(matches_for_path, 1):
            if not isinstance(match, dict):
                raise ValueError(f"Malformed occurrence in {path}")
            line = match.get("line")
            if isinstance(line, bool) or not isinstance(line, int) or line < 1:
                raise ValueError(f"Invalid line number in {path}: {line!r}")
            if not isinstance(match.get("text"), str):
                raise ValueError(f"Missing matched text in {path}:{line}")
            oid = occurrence_id(ref_name, path, line, index)
            if oid in seen_occurrences:
                raise ValueError(f"Duplicate occurrence identity: {oid}")
            seen_occurrences.add(oid)

    return ref


def build_ledger(inventory: dict, ref: dict, inventory_sha256: str) -> dict:
    ref_name = ref["ref_requested"]
    rows: list[dict[str, Any]] = []

    for entry in ref["entries"]:
        path = entry["path"]
        for index, match in enumerate(entry["matches"], 1):
            row = {
                "occurrence_id": occurrence_id(
                    ref_name, path, match["line"], index
                ),
                "repository_ref": ref_name,
                "commit_sha": ref["commit_sha"],
                "path": path,
                "line": match["line"],
                "exact_matched_text": match["text"],
                "automated_inventory_classification": match.get(
                    "classification", "UNKNOWN"
                ),
            }
            row["occurrence_local_assessment"] = classify_occurrence(
                path=path,
                line=match["line"],
                matched_text=match["text"],
                context_window=match.get("context_window"),
            )
            row.update(INITIAL_FIELDS)
            rows.append(row)

    rows.sort(key=lambda row: (row["path"], row["line"], row["occurrence_id"]))
    return {
        "schema": LEDGER_SCHEMA,
        "inventory_commit": ref["commit_sha"],
        "inventory_ref": ref_name,
        "inventory_sha256": inventory_sha256,
        "occurrence_count": len(rows),
        "authority": "DISCOVERY_TEMPLATE_ONLY_NOT_APPROVAL",
        "records": rows,
    }


def reconcile_inventory_and_ledger(inventory: dict, ref: dict, ledger: dict) -> dict:
    expected: dict[str, tuple] = {}
    for entry in ref["entries"]:
        for index, match in enumerate(entry["matches"], 1):
            oid = occurrence_id(ref["ref_requested"], entry["path"], match["line"], index)
            expected[oid] = (
                ref["commit_sha"], entry["path"], match["line"], match["text"],
                match.get("classification", "UNKNOWN"),
            )

    observed: dict[str, tuple] = {}
    duplicate_ids: list[str] = []
    records = ledger.get("records") if isinstance(ledger, dict) else None
    if not isinstance(records, list):
        records = []

    for row in records:
        if not isinstance(row, dict):
            continue
        oid = row.get("occurrence_id")
        if not isinstance(oid, str):
            continue
        if oid in observed:
            duplicate_ids.append(oid)
        observed[oid] = (
            row.get("commit_sha"), row.get("path"), row.get("line"),
            row.get("exact_matched_text"),
            row.get("automated_inventory_classification"),
        )

    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    mismatched = sorted(
        oid for oid in set(expected) & set(observed)
        if expected[oid] != observed[oid]
    )
    identity_ok = (
        ledger.get("schema") == LEDGER_SCHEMA
        and ledger.get("inventory_commit") == ref["commit_sha"]
        and ledger.get("inventory_ref") == ref["ref_requested"]
    )
    count_ok = ledger.get("occurrence_count") == len(records) == len(expected)
    passed = identity_ok and count_ok and not missing and not extra and not mismatched and not duplicate_ids

    return {
        "schema": RECONCILIATION_SCHEMA,
        "status": "RECONCILED" if passed else "RECONCILIATION_FAILED",
        "diagnostic_only": True,
        "authority": "NO_CLASSIFICATION_OR_EXECUTION_AUTHORITY",
        "inventory_commit": ref["commit_sha"],
        "inventory_ref": ref["ref_requested"],
        "expected_occurrence_count": len(expected),
        "observed_occurrence_count": len(records),
        "ledger_declared_occurrence_count": ledger.get("occurrence_count"),
        "identity_matches": identity_ok,
        "count_matches": count_ok,
        "missing_occurrence_ids": missing,
        "extra_occurrence_ids": extra,
        "duplicate_occurrence_ids": sorted(set(duplicate_ids)),
        "identity_field_mismatches": mismatched,
        "manual_review_state_preserved": all(
            row.get("status") in {"OPEN", "CLOSED"}
            and row.get("manual_classification") is not None
            for row in records if isinstance(row, dict)
        ),
        "interpretation": (
            "Reconciliation verifies occurrence identity and coverage only. "
            "It does not validate manual classifications, call paths, guards, "
            "statistical results, protocol approval, or scientific claims."
        ),
    }


def generate(inventory_path: Path, expected_commit: str, ledger_path: Path, reconciliation_path: Path) -> dict:
    inventory_path = Path(inventory_path)
    data = json.loads(inventory_path.read_text(encoding="utf-8"))
    ref = _validate_inventory(data, expected_commit)
    inventory_hash = sha256_file(inventory_path)
    ledger = build_ledger(data, ref, inventory_hash)
    reconciliation = reconcile_inventory_and_ledger(data, ref, ledger)

    ledger_path = Path(ledger_path)
    reconciliation_path = Path(reconciliation_path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    reconciliation_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_bytes(canonical_json_bytes(ledger))
    reconciliation_path.write_bytes(canonical_json_bytes(reconciliation))

    if reconciliation["status"] != "RECONCILED":
        raise ValueError("Generated ledger did not reconcile with its source inventory")
    return reconciliation


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an unresolved Type-I occurrence ledger from an exact inventory."
    )
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument(
        "--output-ledger",
        default="artifacts/type1_occurrence_ledger/occurrence_level_manual_ledger.json",
    )
    parser.add_argument(
        "--output-reconciliation",
        default="artifacts/type1_occurrence_ledger/reconciliation.json",
    )
    args = parser.parse_args()

    try:
        report = generate(
            Path(args.inventory), args.expected_commit,
            Path(args.output_ledger), Path(args.output_reconciliation),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"BLOCKED: {exc}") from exc

    print(
        "Occurrence ledger generated and reconciled: "
        f"{report['observed_occurrence_count']} occurrences."
    )
    print("All records remain discovery-only and OPEN.")
    print("No protocol, threshold, claim, or authorization state was changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
