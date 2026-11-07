from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

OVERLAY_SCHEMA = "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V3"

HIGH_CLASSES = {
    "EXECUTION_ENTRY_POINT",
    "EXECUTION_CALLER",
    "WORKFLOW_TRIGGER_OR_CONTROL",
    "AUTHORIZATION_GUARD",
}

CLASSES = HIGH_CLASSES | {
    "TEST_ONLY",
    "DOCUMENTATION_ONLY",
    "HISTORICAL_OR_SUPERSEDED",
    "DIAGNOSTIC_ONLY",
    "POLICY_OR_CONFIGURATION",
    "NON_EXECUTABLE_REFERENCE",
    "UNRESOLVED",
}

PLACEHOLDERS = {
    "", "OPEN", "UNKNOWN", "UNRESOLVED",
    "NOT_APPLICABLE", "NONE", "MISSING",
    "NOT_YET_IDENTIFIED"
}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object")
    return value


def high_impact(record):
    return (
        record.get("can_influence_execution") in {"YES", "UNRESOLVED"}
        or record.get("manual_classification") in HIGH_CLASSES
        or record.get("manual_classification") == "UNRESOLVED"
    )


def validate_record(record):
    oid = record.get("occurrence_id", "<missing>")

    required = [
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
        "closure_evidence",
        "second_review"
    ]

    for key in required:
        if key not in record:
            raise ValueError(f"{oid}: missing {key}")

        if key not in {"closure_evidence", "second_review"}:
            if not isinstance(record[key], str) or not record[key].strip():
                raise ValueError(f"{oid}: {key} must be non-empty")

    if record["reviewer_kind"] != "HUMAN":
        raise ValueError(f"{oid}: primary reviewer must be human")

    if record["manual_classification"] not in CLASSES:
        raise ValueError(f"{oid}: invalid classification")

    if record["can_influence_execution"] not in {
        "YES", "NO", "UNRESOLVED"
    }:
        raise ValueError(f"{oid}: invalid execution influence")

    if record["status"] not in {"OPEN", "CLOSED"}:
        raise ValueError(f"{oid}: invalid status")

    if record["reviewer_disposition"] not in {
        "ADJUDICATED", "PENDING"
    }:
        raise ValueError(f"{oid}: invalid disposition")

    second = record["second_review"]

    if not isinstance(second, dict):
        raise ValueError(f"{oid}: second_review must be an object")

    second_status = second.get("status")

    if second_status not in {
        "NOT_REQUIRED", "PENDING", "AGREED", "DISAGREED"
    }:
        raise ValueError(f"{oid}: invalid second-review status")

    if second_status == "NOT_REQUIRED" and high_impact(record):
        raise ValueError(f"{oid}: high-impact record cannot waive second review")

    if second_status in {"AGREED", "DISAGREED"}:
        if second.get("reviewer_kind") != "HUMAN":
            raise ValueError(f"{oid}: second reviewer must be human")

        for key in (
            "reviewer", "reviewer_role", "conflict_statement",
            "reviewed_at_utc", "rationale"
        ):
            if not isinstance(second.get(key), str) or not second[key].strip():
                raise ValueError(f"{oid}: second-review {key} missing")

        if second["reviewer"].strip().casefold() == record["reviewer"].strip().casefold():
            raise ValueError(f"{oid}: second reviewer must be a distinct human")

    if second_status == "DISAGREED" and record["status"] == "CLOSED":
        raise ValueError(f"{oid}: disagreement must remain OPEN")

    if record["status"] == "CLOSED":
        if record["reviewer_disposition"] != "ADJUDICATED":
            raise ValueError(f"{oid}: CLOSED requires ADJUDICATED")

        if (
            record["manual_classification"] == "UNRESOLVED"
            or record["can_influence_execution"] == "UNRESOLVED"
        ):
            raise ValueError(f"{oid}: unresolved record cannot close")

        if high_impact(record) and second_status != "AGREED":
            raise ValueError(
                f"{oid}: high-impact CLOSED requires AGREED second review"
            )

        evidence = record["closure_evidence"]

        if not isinstance(evidence, dict):
            raise ValueError(f"{oid}: closure evidence required")

        if not evidence.get("references"):
            raise ValueError(f"{oid}: exact evidence references required")

        if not evidence.get("description"):
            raise ValueError(f"{oid}: evidence description required")

        if evidence.get("negative_test_passed") is not True:
            raise ValueError(f"{oid}: negative test must have passed")

        if record["negative_test"].strip().upper() in PLACEHOLDERS:
            raise ValueError(f"{oid}: missing negative test")

        for key in (
            "direct_caller_or_workflow_step",
            "indirect_call_path",
            "runner_entry_point_or_command",
            "trigger_conditions_and_branch_restrictions",
            "authorization_guard_and_execution_order"
        ):
            if record[key].strip().upper() in PLACEHOLDERS:
                raise ValueError(f"{oid}: CLOSED requires specific {key}")

    elif record["closure_evidence"] is not None:
        raise ValueError(f"{oid}: OPEN requires null closure_evidence")


def merge(inventory_path, ledger_path, overlay_path, output_path):
    inventory = read_json(inventory_path)
    ledger = read_json(ledger_path)
    overlay = read_json(overlay_path)

    inventory_sha = sha256_file(inventory_path)

    if overlay.get("schema") != OVERLAY_SCHEMA:
        raise ValueError("Unsupported V3 overlay schema")

    if overlay.get("inventory_sha256") != inventory_sha:
        raise ValueError("Inventory SHA-256 mismatch")

    commit = overlay.get("review_commit_sha")

    if ledger.get("inventory_commit", "").lower() != commit.lower():
        raise ValueError("Ledger commit mismatch")

    if ledger.get("inventory_sha256") != inventory_sha:
        raise ValueError("Ledger inventory mismatch")

    if ledger.get("inventory_ref") != overlay.get("inventory_ref"):
        raise ValueError("Inventory ref mismatch")

    decisions = overlay.get("records")

    if not isinstance(decisions, list):
        raise ValueError("Overlay records must be a list")

    by_id = {}

    for record in decisions:
        validate_record(record)
        oid = record["occurrence_id"]

        if oid in by_id:
            raise ValueError(f"Duplicate overlay ID: {oid}")

        by_id[oid] = record

    ledger_rows = ledger.get("records", [])
    ledger_ids = [row["occurrence_id"] for row in ledger_rows]

    if len(ledger_ids) != len(set(ledger_ids)):
        raise ValueError("Duplicate ledger occurrence IDs")

    if not set(by_id).issubset(set(ledger_ids)):
        raise ValueError("Overlay contains unknown occurrence IDs")

    merged = []

    for row in ledger_rows:
        updated = dict(row)
        decision = by_id.get(row["occurrence_id"])

        if decision:
            for key, value in decision.items():
                updated[key] = value

        merged.append(updated)

    result = dict(ledger)
    result["records"] = merged
    result["manual_adjudication_overlay"] = {
        "schema": OVERLAY_SCHEMA,
        "inventory_sha256": inventory_sha,
        "overlay_sha256": sha256_file(overlay_path),
        "record_count": len(by_id),
        "authority": "NO_CLASSIFICATION_OR_EXECUTION_AUTHORITY"
    }

    result["protocol_freeze"] = "NOT_FROZEN"
    result["formal_calibration_authorized"] = False
    result["confirmatory_execution_authorized"] = False
    result["claim_support"] = False
    result["promotion_authority"] = False

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    return {
        "merged": len(merged),
        "adjudicated": len(by_id),
        "open": sum(r["status"] == "OPEN" for r in merged),
        "closed": sum(r["status"] == "CLOSED" for r in merged),
        "inventory_sha256": inventory_sha,
        "authority": "NONE"
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--overlay", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = merge(
        args.inventory,
        args.ledger,
        args.overlay,
        args.output
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
