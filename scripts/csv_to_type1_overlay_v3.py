#!/usr/bin/env python3
"""Convert completed V3 CSV decisions into a commit-bound JSON overlay."""

import argparse
import csv
import json
from pathlib import Path

FIELDS = (
    "occurrence_id",
    "manual_classification",
    "can_influence_execution",
    "direct_caller_or_workflow_step",
    "indirect_call_path",
    "runner_entry_point_or_command",
    "trigger_conditions_and_branch_restrictions",
    "matrix_and_protocol_consumed",
    "authorization_guard_and_execution_order",
    "guard_fails_closed",
    "negative_test",
    "test_run_job_artifact_commit",
    "historical_diagnostic_proposed_governance_status",
    "reviewer",
    "reviewer_kind",
    "reviewer_role",
    "conflict_statement",
    "reviewed_at_utc",
    "rationale",
    "status",
    "reviewer_disposition",
)


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
    metadata = (
        "inventory_commit",
        "inventory_ref",
        "inventory_sha256",
    )

    if any(not first.get(key) for key in metadata):
        raise SystemExit("Missing inventory binding")

    for row in rows:
        if any(row.get(key) != first[key] for key in metadata):
            raise SystemExit("Mixed inventory identity in CSV")

    records = []

    for line_number, row in enumerate(rows, start=2):
        if (row.get("reviewer_disposition") or "PENDING").strip() != "ADJUDICATED":
            continue

        record = {
            key: (row.get(key) or "").strip()
            for key in FIELDS
        }

        for key in ("closure_evidence", "second_review"):
            raw = (row.get(key) or "").strip()

            if not raw:
                raise SystemExit(
                    f"CSV row {line_number}: missing {key} JSON"
                )

            try:
                record[key] = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SystemExit(
                    f"CSV row {line_number}: invalid {key}: {exc}"
                )

        records.append(record)

    overlay = {
        "schema": "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V3",
        "review_commit_sha": first["inventory_commit"],
        "inventory_ref": first["inventory_ref"],
        "inventory_sha256": first["inventory_sha256"],
        "records": records,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(overlay, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"V3_OVERLAY_WRITTEN records={len(records)} "
        f"csv_rows={len(rows)}"
    )
    print("PENDING rows remain OPEN in the source ledger.")


if __name__ == "__main__":
    main()
