from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


INVENTORY_SCHEMA = "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1"
OVERLAY_SCHEMA = "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def inventory_identity(
    inventory: dict,
    expected_commit: str,
) -> tuple[str, set[str]]:
    if inventory.get("audit") != INVENTORY_SCHEMA:
        raise ValueError("Unsupported inventory schema")

    refs = inventory.get("refs")
    if not isinstance(refs, list):
        raise ValueError("Inventory refs must be a list")

    matches = [
        item for item in refs
        if isinstance(item, dict)
        and item.get("commit_sha", "").lower()
        == expected_commit.lower()
    ]
    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one inventory ref for review commit"
        )

    ref = matches[0]
    ref_name = ref.get("ref_requested")
    entries = ref.get("entries")

    if not isinstance(ref_name, str) or not ref_name:
        raise ValueError("Missing inventory ref_requested")
    if not isinstance(entries, list):
        raise ValueError("Inventory entries must be a list")

    occurrence_ids: set[str] = set()

    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Malformed inventory entry")

        path = entry.get("path")
        found = entry.get("matches")

        if not isinstance(path, str) or not path:
            raise ValueError("Invalid inventory path")
        if path.startswith("/") or ".." in Path(path).parts:
            raise ValueError(f"Unsafe inventory path: {path}")
        if not isinstance(found, list):
            raise ValueError(f"Malformed matches for {path}")

        path_hash = hashlib.sha256(
            path.encode("utf-8")
        ).hexdigest()[:12]

        for index, match in enumerate(found, 1):
            if not isinstance(match, dict):
                raise ValueError(f"Malformed match in {path}")

            line = match.get("line")
            if isinstance(line, bool) or not isinstance(line, int) or line < 1:
                raise ValueError(f"Invalid line in {path}")

            occurrence_id = (
                f"{ref_name}/{path_hash}/{line}/{index}"
            )

            if occurrence_id in occurrence_ids:
                raise ValueError(
                    f"Duplicate inventory occurrence ID: {occurrence_id}"
                )

            occurrence_ids.add(occurrence_id)

    return ref_name, occurrence_ids


def validate_overlay_record(
    record: dict,
    valid_ids: set[str],
) -> str:
    occurrence_id = record.get("occurrence_id")

    if not isinstance(occurrence_id, str) or not occurrence_id:
        raise ValueError("Overlay record missing occurrence_id")

    if occurrence_id not in valid_ids:
        raise ValueError(
            f"Unknown occurrence ID: {occurrence_id}"
        )

    classification = record.get("manual_classification")
    if not isinstance(classification, str) or not classification.strip():
        raise ValueError("Missing manual classification")

    status = record.get("status")
    if status not in {"OPEN", "CLOSED"}:
        raise ValueError("status must be OPEN or CLOSED")

    if record.get("reviewer_disposition") != "ADJUDICATED":
        raise ValueError(
            "Overlay records require an explicit human adjudication"
        )

    for field in ("reviewer", "reviewed_at_utc", "rationale"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing human review field: {field}")

    evidence = record.get("closure_evidence")

    if status == "CLOSED":
        if classification == "UNKNOWN":
            raise ValueError("UNKNOWN cannot be CLOSED")

        if not isinstance(evidence, dict):
            raise ValueError(
                "CLOSED requires a closure_evidence object"
            )

        for field in ("reference", "description"):
            value = evidence.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"CLOSED requires closure evidence {field}"
                )

    elif evidence is not None:
        raise ValueError(
            "OPEN records must not claim closure evidence"
        )

    return occurrence_id


def merge_overlay(
    inventory_path: Path,
    ledger_path: Path,
    overlay_path: Path,
    output_path: Path,
) -> dict:
    inventory_sha = sha256_file(inventory_path)
    inventory = read_json(inventory_path)
    ledger = read_json(ledger_path)
    overlay = read_json(overlay_path)

    if overlay.get("schema") != OVERLAY_SCHEMA:
        raise ValueError("Unsupported overlay schema")

    review_commit = overlay.get("review_commit_sha")
    if not isinstance(review_commit, str) or len(review_commit) != 40:
        raise ValueError("Invalid overlay review_commit_sha")

    if overlay.get("inventory_sha256") != inventory_sha:
        raise ValueError("Overlay inventory SHA-256 mismatch")

    inventory_ref, valid_ids = inventory_identity(
        inventory,
        review_commit,
    )

    if overlay.get("inventory_ref") != inventory_ref:
        raise ValueError("Overlay inventory_ref mismatch")

    if ledger.get("inventory_commit", "").lower() != review_commit.lower():
        raise ValueError("Ledger review commit mismatch")

    if ledger.get("inventory_sha256") != inventory_sha:
        raise ValueError("Ledger inventory SHA-256 mismatch")

    if ledger.get("inventory_ref") != inventory_ref:
        raise ValueError("Ledger inventory_ref mismatch")

    records = overlay.get("records")
    if not isinstance(records, list):
        raise ValueError("Overlay records must be a list")

    overlay_by_id: dict[str, dict] = {}

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Overlay record must be an object")

        occurrence_id = validate_overlay_record(
            record,
            valid_ids,
        )

        if occurrence_id in overlay_by_id:
            raise ValueError(
                f"Duplicate/conflicting overlay ID: {occurrence_id}"
            )

        overlay_by_id[occurrence_id] = record

    ledger_records = ledger.get("records")
    if not isinstance(ledger_records, list):
        raise ValueError("Ledger records must be a list")

    ledger_by_id = {}
    for row in ledger_records:
        occurrence_id = row.get("occurrence_id")
        if not isinstance(occurrence_id, str):
            raise ValueError("Ledger row missing occurrence_id")
        if occurrence_id in ledger_by_id:
            raise ValueError(
                f"Duplicate ledger ID: {occurrence_id}"
            )
        ledger_by_id[occurrence_id] = row

    if set(ledger_by_id) != valid_ids:
        raise ValueError(
            "Ledger and inventory occurrence identities differ"
        )

    for occurrence_id, decision in overlay_by_id.items():
        row = ledger_by_id[occurrence_id]

        row["manual_classification"] = decision[
            "manual_classification"
        ]
        row["status"] = decision["status"]
        row["reviewer_disposition"] = "ADJUDICATED"
        row["adjudication_rationale"] = decision["rationale"]
        row["reviewer_identity"] = decision["reviewer"]
        row["reviewed_at_utc"] = decision["reviewed_at_utc"]
        row["closure_evidence"] = decision.get("closure_evidence")

    result = dict(ledger)
    result["records"] = ledger_records
    result["manual_adjudication_overlay"] = {
        "schema": OVERLAY_SCHEMA,
        "inventory_sha256": inventory_sha,
        "review_commit_sha": review_commit,
        "overlay_record_count": len(overlay_by_id),
        "overlay_sha256": sha256_file(overlay_path),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=output_path.name + ".",
        suffix=".tmp",
        dir=str(output_path.parent),
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(
                result,
                stream,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
            stream.write("\n")

        os.replace(temp_name, output_path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--overlay", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    merge_overlay(
        Path(args.inventory),
        Path(args.ledger),
        Path(args.overlay),
        Path(args.output),
    )

    print("OVERLAY_MERGE_SUCCESS")
    print("Unreviewed records remain unchanged.")
    print("No execution or protocol authority is granted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
