#!/usr/bin/env python3
"""Convert a single-inventory V3 adjudication CSV to a JSON overlay."""

import argparse
import csv
import json
from pathlib import Path

FIELDS = (
    "occurrence_id", "manual_classification", "can_influence_execution",
    "direct_caller_or_workflow_step", "indirect_call_path",
    "runner_entry_point_or_command", "trigger_conditions_and_branch_restrictions",
    "matrix_and_protocol_consumed", "authorization_guard_and_execution_order",
    "guard_fails_closed", "negative_test", "test_run_job_artifact_commit",
    "historical_diagnostic_proposed_governance_status", "reviewer", "reviewer_kind",
    "reviewer_role", "conflict_statement", "reviewed_at_utc", "rationale", "status",
    "reviewer_disposition",
)
METADATA = ("inventory_commit", "inventory_ref", "inventory_sha256")
JSON_FIELDS = ("closure_evidence", "second_review")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.csv, encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise SystemExit("No CSV rows")

    first = rows[0]
    if any(not (first.get(key) or "").strip() for key in METADATA):
        raise SystemExit("Missing inventory binding metadata")
    for key in METADATA:
        if key == "inventory_commit" and len(first[key].strip()) != 40:
            raise SystemExit("inventory_commit must be a full 40-character commit SHA")
        if key == "inventory_sha256" and len(first[key].strip()) != 64:
            raise SystemExit("inventory_sha256 must be a full SHA-256 digest")
    for row_number, row in enumerate(rows, start=2):
        for key in METADATA:
            if (row.get(key) or "").strip() != first[key].strip():
                raise SystemExit(f"CSV row {row_number}: mixed inventory identity ({key})")

    records = []
    seen = set()
    for row_number, row in enumerate(rows, start=2):
        disposition = (row.get("reviewer_disposition") or "PENDING").strip()
        if disposition == "PENDING":
            continue
        if disposition != "ADJUDICATED":
            raise SystemExit(f"CSV row {row_number}: invalid reviewer_disposition")
        record = {key: (row.get(key) or "").strip() for key in FIELDS}
        for key in JSON_FIELDS:
            raw = (row.get(key) or "").strip()
            if not raw:
                raise SystemExit(f"CSV row {row_number}: missing {key} JSON")
            try:
                record[key] = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"CSV row {row_number}: invalid {key}: {exc}")
        oid = record["occurrence_id"]
        if not oid:
            raise SystemExit(f"CSV row {row_number}: missing occurrence_id")
        if oid in seen:
            raise SystemExit(f"CSV row {row_number}: duplicate occurrence_id {oid}")
        seen.add(oid)
        records.append(record)

    overlay = {
        "schema": "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V3",
        "review_commit_sha": first["inventory_commit"].strip(),
        "inventory_ref": first["inventory_ref"].strip(),
        "inventory_sha256": first["inventory_sha256"].strip(),
        "records": records,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(overlay, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"V3_OVERLAY_WRITTEN records={len(records)} csv_rows={len(rows)}")
    print("PENDING rows are not imported; source-ledger rows remain OPEN.")
    print("This converter does not grant execution, calibration, claim, or promotion authority.")


if __name__ == "__main__":
    main()
