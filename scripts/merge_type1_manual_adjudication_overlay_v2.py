from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

INVENTORY_SCHEMA = "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1"
OVERLAY_SCHEMA = "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V2"
CLASSES = {
    "EXECUTION_ENTRY_POINT", "EXECUTION_CALLER", "WORKFLOW_TRIGGER_OR_CONTROL",
    "AUTHORIZATION_GUARD", "TEST_ONLY", "DOCUMENTATION_ONLY",
    "HISTORICAL_OR_SUPERSEDED", "DIAGNOSTIC_ONLY", "POLICY_OR_CONFIGURATION",
    "NON_EXECUTABLE_REFERENCE", "UNRESOLVED",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def occurrence_id(ref: str, path: str, line: int, index: int) -> str:
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]
    return f"{ref}/{digest}/{line}/{index}"


def inventory_ids(inventory: dict, commit: str) -> tuple[str, set[str]]:
    if inventory.get("audit") != INVENTORY_SCHEMA:
        raise ValueError("Unsupported inventory schema")
    matches = [r for r in inventory.get("refs", [])
               if isinstance(r, dict) and r.get("commit_sha", "").lower() == commit.lower()]
    if len(matches) != 1:
        raise ValueError("Expected exactly one inventory ref for overlay commit")
    ref = matches[0].get("ref_requested")
    if not isinstance(ref, str) or not ref:
        raise ValueError("Inventory ref_requested missing")
    ids: set[str] = set()
    for entry in matches[0].get("entries", []):
        path = entry.get("path")
        if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts:
            raise ValueError(f"Unsafe or missing inventory path: {path!r}")
        for i, match in enumerate(entry.get("matches", []), 1):
            line = match.get("line")
            if isinstance(line, bool) or not isinstance(line, int) or line < 1:
                raise ValueError(f"Invalid line for {path}")
            oid = occurrence_id(ref, path, line, i)
            if oid in ids:
                raise ValueError(f"Duplicate inventory occurrence ID: {oid}")
            ids.add(oid)
    return ref, ids


def validate_record(r: dict, oid: str) -> None:
    required = (
        "manual_classification", "can_influence_execution", "direct_caller_or_workflow_step",
        "indirect_call_path", "runner_entry_point_or_command", "trigger_conditions_and_branch_restrictions",
        "matrix_and_protocol_consumed", "authorization_guard_and_execution_order", "guard_fails_closed",
        "negative_test", "test_run_job_artifact_commit", "historical_diagnostic_proposed_governance_status",
        "reviewer", "reviewer_role", "conflict_statement", "reviewed_at_utc", "rationale",
        "status", "reviewer_disposition", "closure_evidence",
    )
    for key in required:
        if key not in r:
            raise ValueError(f"{oid}: missing required field {key}")
        if key != "closure_evidence" and (not isinstance(r[key], str) or not r[key].strip()):
            raise ValueError(f"{oid}: {key} must be a non-empty string")
    if r["manual_classification"] not in CLASSES:
        raise ValueError(f"{oid}: invalid manual_classification")
    if r["can_influence_execution"] not in {"YES", "NO", "UNRESOLVED"}:
        raise ValueError(f"{oid}: invalid can_influence_execution")
    if r["guard_fails_closed"] not in {"YES", "NO", "UNRESOLVED", "NOT_APPLICABLE"}:
        raise ValueError(f"{oid}: invalid guard_fails_closed")
    if r["status"] not in {"OPEN", "CLOSED"}:
        raise ValueError(f"{oid}: status must be OPEN or CLOSED")
    if r["reviewer_disposition"] != "ADJUDICATED":
        raise ValueError(f"{oid}: record is not explicitly adjudicated")
    if r["manual_classification"] == "UNRESOLVED" and r["status"] == "CLOSED":
        raise ValueError(f"{oid}: UNRESOLVED cannot be CLOSED")
    evidence = r["closure_evidence"]
    if r["status"] == "CLOSED":
        if not isinstance(evidence, dict):
            raise ValueError(f"{oid}: CLOSED requires closure_evidence")
        if not isinstance(evidence.get("references"), list) or not evidence["references"]:
            raise ValueError(f"{oid}: CLOSED requires exact evidence references")
        if not isinstance(evidence.get("description"), str) or not evidence["description"].strip():
            raise ValueError(f"{oid}: CLOSED requires evidence description")
        if evidence.get("negative_test_passed") is not True:
            raise ValueError(f"{oid}: CLOSED requires a passed negative test")
        if r["negative_test"].strip().upper() in {"MISSING", "NOT_YET_IDENTIFIED", "NONE"}:
            raise ValueError(f"{oid}: CLOSED cannot have missing negative-test evidence")
    elif evidence is not None:
        raise ValueError(f"{oid}: OPEN records must have null closure_evidence")
    if r["can_influence_execution"] == "YES":
        for key in ("direct_caller_or_workflow_step", "indirect_call_path", "runner_entry_point_or_command",
                    "trigger_conditions_and_branch_restrictions", "authorization_guard_and_execution_order"):
            if r[key].strip().upper() in {"OPEN", "UNKNOWN", "NOT_APPLICABLE", "NONE"}:
                raise ValueError(f"{oid}: execution-influencing record requires specific {key}")


def merge(inventory_path: Path, ledger_path: Path, overlay_path: Path, output_path: Path,
          require_complete: bool) -> dict:
    inv_sha = sha256_file(inventory_path)
    inv = read_json(inventory_path)
    ledger = read_json(ledger_path)
    overlay = read_json(overlay_path)
    if overlay.get("schema") != OVERLAY_SCHEMA:
        raise ValueError("Unsupported V2 overlay schema")
    commit = overlay.get("review_commit_sha")
    if not isinstance(commit, str) or len(commit) != 40:
        raise ValueError("Invalid review_commit_sha")
    if overlay.get("inventory_sha256") != inv_sha:
        raise ValueError("Overlay inventory SHA-256 mismatch")
    ref, expected_ids = inventory_ids(inv, commit)
    if overlay.get("inventory_ref") != ref:
        raise ValueError("Overlay inventory_ref mismatch")
    if ledger.get("inventory_commit", "").lower() != commit.lower():
        raise ValueError("Ledger commit mismatch")
    if ledger.get("inventory_ref") != ref or ledger.get("inventory_sha256") != inv_sha:
        raise ValueError("Ledger inventory identity mismatch")
    rows = ledger.get("records")
    if not isinstance(rows, list):
        raise ValueError("Ledger records must be a list")
    by_id = {r.get("occurrence_id"): r for r in rows}
    if len(by_id) != len(rows) or set(by_id) != expected_ids:
        raise ValueError("Ledger occurrence IDs do not exactly match inventory IDs")
    decisions = overlay.get("records")
    if not isinstance(decisions, list):
        raise ValueError("Overlay records must be a list")
    decisions_by_id = {}
    for r in decisions:
        if not isinstance(r, dict):
            raise ValueError("Overlay record must be an object")
        oid = r.get("occurrence_id")
        if oid not in expected_ids:
            raise ValueError(f"Unknown occurrence ID: {oid}")
        if oid in decisions_by_id:
            raise ValueError(f"Duplicate overlay occurrence ID: {oid}")
        validate_record(r, oid)
        decisions_by_id[oid] = r
    if require_complete and set(decisions_by_id) != expected_ids:
        raise ValueError(f"Incomplete overlay: {len(expected_ids - set(decisions_by_id))} occurrence IDs unreviewed")
    merged = []
    mapped = {
        "manual_classification": "manual_classification",
        "can_influence_execution": "can_influence_execution",
        "direct_caller_or_workflow_step": "direct_caller_or_workflow_step",
        "indirect_call_path": "indirect_call_path",
        "runner_entry_point_or_command": "runner_entry_point_or_command",
        "trigger_conditions_and_branch_restrictions": "trigger_conditions_and_branch_restrictions",
        "matrix_and_protocol_consumed": "matrix_and_protocol_consumed",
        "authorization_guard_and_execution_order": "authorization_guard_and_execution_order",
        "guard_fails_closed": "guard_fails_closed",
        "negative_test": "negative_test",
        "test_run_job_artifact_commit": "test_run_job_artifact_commit",
        "historical_diagnostic_proposed_governance_status": "historical_diagnostic_proposed_governance_status",
        "reviewer_disposition": "reviewer_disposition",
        "status": "status",
        "closure_evidence": "closure_evidence",
    }
    for row in rows:
        new = dict(row)
        decision = decisions_by_id.get(row["occurrence_id"])
        if decision:
            for src, dst in mapped.items(): new[dst] = decision[src]
            new["reviewer_identity"] = decision["reviewer"]
            new["reviewer_role"] = decision["reviewer_role"]
            new["reviewer_conflict_statement"] = decision["conflict_statement"]
            new["reviewed_at_utc"] = decision["reviewed_at_utc"]
            new["adjudication_rationale"] = decision["rationale"]
            new["manual_adjudication_schema"] = OVERLAY_SCHEMA
        merged.append(new)
    result = dict(ledger)
    result["records"] = merged
    result["manual_adjudication_overlay"] = {
        "schema": OVERLAY_SCHEMA,
        "inventory_sha256": inv_sha,
        "review_commit_sha": commit,
        "overlay_sha256": sha256_file(overlay_path),
        "adjudicated_record_count": len(decisions_by_id),
        "expected_record_count": len(expected_ids),
        "complete": set(decisions_by_id) == expected_ids,
        "authority": "HUMAN_ADJUDICATION_RECORD_ONLY_NO_EXECUTION_OR_PROTOCOL_AUTHORITY",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=output_path.name + ".", suffix=".tmp", dir=str(output_path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, sort_keys=True, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, output_path)
    except Exception:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--inventory", required=True)
    p.add_argument("--ledger", required=True)
    p.add_argument("--overlay", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--require-complete", action="store_true")
    a = p.parse_args()
    result = merge(Path(a.inventory), Path(a.ledger), Path(a.overlay), Path(a.output), a.require_complete)
    print(json.dumps(result["manual_adjudication_overlay"], indent=2))
    print("MERGE_COMPLETE; NO_EXECUTION_OR_PROTOCOL_AUTHORITY_GRANTED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
