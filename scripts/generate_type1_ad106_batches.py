from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_COMMIT = "ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876"
EXPECTED_INVENTORY_SHA256 = (
    "88222e3178bc62854ffb8d1fa961c1fb4cfe582c9ff1082878ab759e011cc635"
)
EXPECTED_COUNT = 1800
BATCH_SIZE = 50

def canonical_json(data):
    return (
        json.dumps(
            data,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ) + "\n"
    ).encode("utf-8")

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    ledger_path = Path(args.ledger)
    out_dir = Path(args.output_dir)

    ledger_bytes = ledger_path.read_bytes()
    ledger = json.loads(ledger_bytes)

    if ledger.get("schema") != "HCM_TYPE1_OCCURRENCE_MANUAL_LEDGER_V1":
        raise SystemExit("BLOCKED: unexpected ledger schema.")

    if ledger.get("inventory_commit") != EXPECTED_COMMIT:
        raise SystemExit("BLOCKED: target commit mismatch.")

    if ledger.get("inventory_sha256") != EXPECTED_INVENTORY_SHA256:
        raise SystemExit("BLOCKED: inventory hash mismatch.")

    records = ledger.get("records")
    if not isinstance(records, list) or len(records) != EXPECTED_COUNT:
        raise SystemExit("BLOCKED: expected exactly 1800 records.")

    ids = []
    for row in records:
        if row.get("commit_sha") != EXPECTED_COMMIT:
            raise SystemExit("BLOCKED: mixed commit identities.")
        if row.get("repository_ref") != "refs/audit/target":
            raise SystemExit("BLOCKED: mixed repository refs.")
        if row.get("status") != "OPEN":
            raise SystemExit("BLOCKED: unexpected adjudication state.")
        if row.get("manual_classification") != "UNKNOWN":
            raise SystemExit("BLOCKED: manual classification was altered.")

        oid = row.get("occurrence_id")
        if not isinstance(oid, str) or not oid:
            raise SystemExit("BLOCKED: missing occurrence ID.")
        ids.append(oid)

    if len(ids) != len(set(ids)):
        raise SystemExit("BLOCKED: duplicate occurrence IDs.")

    if len(ids) != EXPECTED_COUNT:
        raise SystemExit("BLOCKED: occurrence count changed.")

    out_dir.mkdir(parents=True, exist_ok=True)
    batch_registers = []

    for offset in range(0, len(ids), BATCH_SIZE):
        batch_ids = ids[offset:offset + BATCH_SIZE]
        number = offset // BATCH_SIZE + 1
        batch_id = f"AD106_B{number:03d}"

        canonical_ids = ("\n".join(batch_ids) + "\n").encode("utf-8")

        batch = {
            "schema": "HCM_TYPE1_ADJUDICATION_BATCH_REGISTER_V3",
            "batch_id": batch_id,
            "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
            "target_commit": EXPECTED_COMMIT,
            "inventory_ref": "refs/audit/target",
            "inventory_sha256": EXPECTED_INVENTORY_SHA256,
            "count": len(batch_ids),
            "first_occurrence_id": batch_ids[0],
            "last_occurrence_id": batch_ids[-1],
            "canonical_id_sequence_sha256": sha256_bytes(canonical_ids),
            "canonicalization": (
                "UTF-8; one occurrence ID per line; final newline included"
            ),
            "occurrence_ids": batch_ids,
            "primary_reviewer": None,
            "second_reviewer_policy": (
                "Distinct human second review required for every "
                "high-impact occurrence. AI is not a reviewer."
            ),
            "authority": "NONE",
            "protocol_freeze": "NOT_FROZEN",
            "formal_calibration_authorized": False,
            "confirmatory_execution_authorized": False,
            "claim_support": False,
            "promotion_authority": False,
        }

        filename = f"TYPE1_BATCH_REGISTER_{batch_id}.json"
        (out_dir / filename).write_bytes(canonical_json(batch))
        batch_registers.append({
            "batch_id": batch_id,
            "file": filename,
            "count": len(batch_ids),
            "first": batch_ids[0],
            "last": batch_ids[-1],
            "sha256": sha256_bytes(canonical_ids),
        })

    if sum(x["count"] for x in batch_registers) != EXPECTED_COUNT:
        raise SystemExit("BLOCKED: batch coverage mismatch.")

    index = {
        "schema": "HCM_TYPE1_AD106_BATCH_INDEX_V1",
        "target_commit": EXPECTED_COMMIT,
        "inventory_ref": "refs/audit/target",
        "inventory_sha256": EXPECTED_INVENTORY_SHA256,
        "total_occurrences": EXPECTED_COUNT,
        "batch_size": BATCH_SIZE,
        "batch_count": len(batch_registers),
        "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
        "batches": batch_registers,
        "authority": "NONE",
    }

    (out_dir / "TYPE1_AD106_BATCH_INDEX.json").write_bytes(
        canonical_json(index)
    )

    print(json.dumps({
        "status": "BATCHES_GENERATED",
        "batch_count": len(batch_registers),
        "occurrence_count": EXPECTED_COUNT,
        "all_ids_unique": True,
        "inventory_sha256": EXPECTED_INVENTORY_SHA256,
        "authority": "NONE",
    }, indent=2))

if __name__ == "__main__":
    main()
