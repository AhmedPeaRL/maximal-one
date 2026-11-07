from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath

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
    "", "OPEN", "UNKNOWN", "UNRESOLVED", "NOT_APPLICABLE", "NONE",
    "MISSING", "NOT_YET_IDENTIFIED", "PENDING",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path: str | Path) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _is_placeholder(value: object) -> bool:
    return not isinstance(value, str) or value.strip().upper() in PLACEHOLDERS


def _valid_utc(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def high_impact(record: dict) -> bool:
    return (
        record.get("can_influence_execution") in {"YES", "UNRESOLVED"}
        or record.get("manual_classification") in HIGH_CLASSES | {"UNRESOLVED"}
    )


def _validate_second_review(record: dict) -> None:
    oid = record.get("occurrence_id", "<missing>")
    second = record.get("second_review")
    if not isinstance(second, dict):
        raise ValueError(f"{oid}: second_review must be an object")
    required = {
        "status", "reviewer", "reviewer_kind", "reviewer_role",
        "conflict_statement", "reviewed_at_utc", "rationale",
    }
    if set(second) != required:
        raise ValueError(f"{oid}: second_review fields must be exactly {sorted(required)}")

    status = second["status"]
    if status not in {"NOT_REQUIRED", "PENDING", "AGREED", "DISAGREED"}:
        raise ValueError(f"{oid}: invalid second-review status")

    if status == "NOT_REQUIRED":
        if high_impact(record):
            raise ValueError(f"{oid}: high-impact record cannot waive second review")
        if second["reviewer_kind"] != "NONE":
            raise ValueError(f"{oid}: NOT_REQUIRED must use reviewer_kind NONE")
        if _is_placeholder(second["rationale"]):
            raise ValueError(f"{oid}: NOT_REQUIRED requires a rationale")
        if record["status"] == "CLOSED" and record["reviewer_disposition"] != "ADJUDICATED":
            raise ValueError(f"{oid}: CLOSED requires ADJUDICATED")
        return

    if status == "PENDING":
        if record["status"] != "OPEN":
            raise ValueError(f"{oid}: PENDING second review requires OPEN status")
        if second["reviewer_kind"] != "NONE":
            raise ValueError(f"{oid}: pending second review must not claim a reviewer")
        if _is_placeholder(second["rationale"]):
            raise ValueError(f"{oid}: pending second review requires a reason")
        return

    if second["reviewer_kind"] != "HUMAN":
        raise ValueError(f"{oid}: completed second review must be human")
    for key in ("reviewer", "reviewer_role", "conflict_statement", "rationale"):
        if _is_placeholder(second[key]):
            raise ValueError(f"{oid}: second-review {key} is missing")
    if not _valid_utc(second["reviewed_at_utc"]):
        raise ValueError(f"{oid}: second-review timestamp must be timezone-aware UTC")
    if second["reviewer"].strip().casefold() == record["reviewer"].strip().casefold():
        raise ValueError(f"{oid}: second reviewer must be distinct from primary reviewer")
    if status == "DISAGREED" and record["status"] != "OPEN":
        raise ValueError(f"{oid}: disagreement must remain OPEN")


def validate_record(record: dict, expected_commit: str | None = None) -> None:
    if not isinstance(record, dict):
        raise ValueError("overlay record must be an object")
    oid = record.get("occurrence_id", "<missing>")
    required = {
        "occurrence_id", "manual_classification", "can_influence_execution",
        "direct_caller_or_workflow_step", "indirect_call_path",
        "runner_entry_point_or_command", "trigger_conditions_and_branch_restrictions",
        "matrix_and_protocol_consumed", "authorization_guard_and_execution_order",
        "guard_fails_closed", "negative_test", "test_run_job_artifact_commit",
        "historical_diagnostic_proposed_governance_status", "reviewer", "reviewer_kind",
        "reviewer_role", "conflict_statement", "reviewed_at_utc", "rationale", "status",
        "reviewer_disposition", "closure_evidence", "second_review",
    }
    if set(record) != required:
        missing, extra = required - set(record), set(record) - required
        raise ValueError(f"{oid}: record keys mismatch; missing={sorted(missing)} extra={sorted(extra)}")

    text_fields = required - {"closure_evidence", "second_review"}
    for key in text_fields:
        if not isinstance(record[key], str) or not record[key].strip():
            raise ValueError(f"{oid}: {key} must be a non-empty string")

    if record["reviewer_kind"] != "HUMAN":
        raise ValueError(f"{oid}: primary reviewer must be HUMAN")
    if not _valid_utc(record["reviewed_at_utc"]):
        raise ValueError(f"{oid}: primary timestamp must be timezone-aware")
    if record["manual_classification"] not in CLASSES:
        raise ValueError(f"{oid}: invalid manual_classification")
    if record["can_influence_execution"] not in {"YES", "NO", "UNRESOLVED"}:
        raise ValueError(f"{oid}: invalid can_influence_execution")
    if record["guard_fails_closed"] not in {"YES", "NO", "UNRESOLVED", "NOT_APPLICABLE"}:
        raise ValueError(f"{oid}: invalid guard_fails_closed")
    if record["status"] not in {"OPEN", "CLOSED"}:
        raise ValueError(f"{oid}: invalid status")
    if record["reviewer_disposition"] not in {"ADJUDICATED", "PENDING"}:
        raise ValueError(f"{oid}: invalid reviewer_disposition")

    _validate_second_review(record)

    if record["status"] == "OPEN":
        if record["closure_evidence"] is not None:
            raise ValueError(f"{oid}: OPEN records must have null closure_evidence")
        return

    if record["reviewer_disposition"] != "ADJUDICATED":
        raise ValueError(f"{oid}: CLOSED requires ADJUDICATED disposition")
    if record["manual_classification"] == "UNRESOLVED" or record["can_influence_execution"] == "UNRESOLVED":
        raise ValueError(f"{oid}: unresolved records cannot close")
    if high_impact(record) and record["second_review"]["status"] != "AGREED":
        raise ValueError(f"{oid}: high-impact CLOSED requires AGREED second human review")

    evidence = record["closure_evidence"]
    if not isinstance(evidence, dict):
        raise ValueError(f"{oid}: CLOSED requires closure_evidence object")
    required_evidence = {
        "references", "description", "negative_test_passed", "negative_test_reference",
        "workflow_run_id", "workflow_job_id", "artifact_id", "commit_sha",
    }
    if set(evidence) != required_evidence:
        raise ValueError(f"{oid}: closure_evidence keys must be exactly {sorted(required_evidence)}")
    if not isinstance(evidence["references"], list) or not evidence["references"]:
        raise ValueError(f"{oid}: exact closure references are required")
    if any(_is_placeholder(item) for item in evidence["references"]):
        raise ValueError(f"{oid}: closure references cannot be placeholders")
    for key in ("description", "negative_test_reference", "workflow_run_id", "workflow_job_id", "artifact_id"):
        if _is_placeholder(evidence[key]):
            raise ValueError(f"{oid}: closure evidence {key} is missing")
    if evidence["negative_test_passed"] is not True:
        raise ValueError(f"{oid}: negative test must have passed")
    if not isinstance(evidence["commit_sha"], str) or not SHA40.fullmatch(evidence["commit_sha"]):
        raise ValueError(f"{oid}: closure evidence commit_sha must be a full SHA")
    if expected_commit and evidence["commit_sha"] != expected_commit:
        raise ValueError(f"{oid}: closure evidence commit does not match reviewed commit")

    for key in (
        "direct_caller_or_workflow_step", "indirect_call_path",
        "runner_entry_point_or_command", "trigger_conditions_and_branch_restrictions",
        "matrix_and_protocol_consumed", "authorization_guard_and_execution_order",
        "negative_test", "test_run_job_artifact_commit",
    ):
        if _is_placeholder(record[key]):
            raise ValueError(f"{oid}: CLOSED requires specific {key}")


def _safe_inventory_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("inventory entry path must be a non-empty string")
    if "\\" in value:
        raise ValueError(f"unsafe inventory path: {value}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ValueError(f"unsafe inventory path: {value}")
    if path.as_posix() != value:
        raise ValueError(f"non-canonical inventory path: {value}")
    return value


def reconstruct_inventory_ids(inventory: dict, inventory_ref: str, commit_sha: str) -> dict[str, tuple[str, int, str]]:
    if inventory.get("audit") != "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1":
        raise ValueError("unsupported inventory audit schema")
    refs = inventory.get("refs")
    if not isinstance(refs, list):
        raise ValueError("inventory refs must be a list")
    selected = [r for r in refs if isinstance(r, dict) and r.get("ref_requested") == inventory_ref and r.get("commit_sha", "").lower() == commit_sha.lower()]
    if len(selected) != 1:
        raise ValueError("inventory must contain exactly one ref matching inventory_ref and review_commit_sha")

    result: dict[str, tuple[str, int, str]] = {}
    seen_paths: set[str] = set()
    for entry in selected[0].get("entries", []):
        if not isinstance(entry, dict):
            raise ValueError("inventory entry must be an object")
        path = _safe_inventory_path(entry.get("path"))
        if path in seen_paths:
            raise ValueError(f"duplicate inventory path: {path}")
        seen_paths.add(path)
        matches = entry.get("matches")
        if not isinstance(matches, list):
            raise ValueError(f"{path}: matches must be a list")
        path_hash = hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]
        for ordinal, match in enumerate(matches, start=1):
            if not isinstance(match, dict):
                raise ValueError(f"{path}: match must be an object")
            line = match.get("line")
            if isinstance(line, bool) or not isinstance(line, int) or line < 1:
                raise ValueError(f"{path}: invalid match line")
            occurrence_id = f"{inventory_ref}/{path_hash}/{line}/{ordinal}"
            if occurrence_id in result:
                raise ValueError(f"duplicate reconstructed inventory ID: {occurrence_id}")
            result[occurrence_id] = (path, line, commit_sha.lower())
    if not result:
        raise ValueError("selected inventory ref contains no occurrences")
    return result


def merge(inventory_path, ledger_path, overlay_path, output_path):
    inventory = read_json(inventory_path)
    ledger = read_json(ledger_path)
    overlay = read_json(overlay_path)
    inventory_sha = sha256_file(inventory_path)

    if overlay.get("schema") != OVERLAY_SCHEMA:
        raise ValueError("unsupported V3 overlay schema")
    commit = overlay.get("review_commit_sha")
    inventory_ref = overlay.get("inventory_ref")
    if not isinstance(commit, str) or not SHA40.fullmatch(commit):
        raise ValueError("overlay review_commit_sha must be a full SHA")
    if not isinstance(inventory_ref, str) or not inventory_ref:
        raise ValueError("overlay inventory_ref is required")
    if overlay.get("inventory_sha256") != inventory_sha:
        raise ValueError("overlay inventory SHA-256 mismatch")

    expected = reconstruct_inventory_ids(inventory, inventory_ref, commit)
    if ledger.get("inventory_commit", "").lower() != commit.lower():
        raise ValueError("ledger commit mismatch")
    if ledger.get("inventory_ref") != inventory_ref:
        raise ValueError("ledger inventory_ref mismatch")
    if ledger.get("inventory_sha256") != inventory_sha:
        raise ValueError("ledger inventory SHA-256 mismatch")

    rows = ledger.get("records")
    if not isinstance(rows, list):
        raise ValueError("ledger records must be a list")
    if ledger.get("occurrence_count") != len(rows):
        raise ValueError("ledger occurrence_count does not match records length")

    ledger_by_id: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("ledger row must be an object")
        oid = row.get("occurrence_id")
        if not isinstance(oid, str) or not oid:
            raise ValueError("ledger row has missing occurrence_id")
        if oid in ledger_by_id:
            raise ValueError(f"duplicate ledger occurrence ID: {oid}")
        if oid not in expected:
            raise ValueError(f"ledger contains ID absent from selected inventory: {oid}")
        path, line, row_commit = expected[oid]
        if row.get("path") != path or row.get("line") != line:
            raise ValueError(f"ledger path/line mismatch for {oid}")
        if row.get("commit_sha", "").lower() != row_commit:
            raise ValueError(f"ledger commit mismatch for {oid}")
        if row.get("repository_ref") != inventory_ref:
            raise ValueError(f"ledger repository_ref mismatch for {oid}")
        ledger_by_id[oid] = row

    expected_ids = set(expected)
    ledger_ids = set(ledger_by_id)
    if ledger_ids != expected_ids:
        missing = sorted(expected_ids - ledger_ids)
        extra = sorted(ledger_ids - expected_ids)
        raise ValueError(f"inventory/ledger ID set mismatch; missing={missing[:5]} extra={extra[:5]}")

    decisions = overlay.get("records")
    if not isinstance(decisions, list):
        raise ValueError("overlay records must be a list")
    decisions_by_id: dict[str, dict] = {}
    for record in decisions:
        validate_record(record, expected_commit=commit)
        oid = record["occurrence_id"]
        if oid in decisions_by_id:
            raise ValueError(f"duplicate overlay occurrence ID: {oid}")
        if oid not in expected_ids:
            raise ValueError(f"overlay occurrence ID absent from verified inventory: {oid}")
        decisions_by_id[oid] = record

    merged = []
    for row in rows:
        updated = dict(row)
        decision = decisions_by_id.get(row["occurrence_id"])
        if decision:
            updated.update(decision)
        merged.append(updated)

    result = dict(ledger)
    result["records"] = merged
    result["manual_adjudication_overlay"] = {
        "schema": OVERLAY_SCHEMA,
        "inventory_sha256": inventory_sha,
        "overlay_sha256": sha256_file(overlay_path),
        "record_count": len(decisions_by_id),
        "authority": "NO_CLASSIFICATION_OR_EXECUTION_AUTHORITY",
    }
    result.update({
        "protocol_freeze": "NOT_FROZEN",
        "formal_calibration_authorized": False,
        "confirmatory_execution_authorized": False,
        "claim_support": False,
        "promotion_authority": False,
    })

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "merged": len(merged),
        "adjudicated_overlay_records": len(decisions_by_id),
        "inventory_sha256": inventory_sha,
        "inventory_ref": inventory_ref,
        "review_commit_sha": commit,
        "authority": "NONE",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--overlay", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(merge(args.inventory, args.ledger, args.overlay, args.output), indent=2))


if __name__ == "__main__":
    main()
