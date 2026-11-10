from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

BATCH_SIZE = 25


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"BLOCKED: expected JSON object: {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path("evidence/occurrence_level_manual_ledger.json"),
    )
    parser.add_argument(
        "--population-register",
        type=Path,
        default=Path("protocol/TYPE1_AD106_POPULATION_REGISTER_V1.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("adjudication/target_1800_batches"),
    )
    args = parser.parse_args()

    ledger = read_json(args.ledger)
    population = read_json(args.population_register)
    target = population["target"]
    inventory = population["inventory"]

    if target.get("commit") != ledger.get("inventory_commit"):
        raise SystemExit("BLOCKED: target commit mismatch.")
    if target.get("ref") != ledger.get("inventory_ref"):
        raise SystemExit("BLOCKED: inventory ref mismatch.")
    if inventory.get("reference_inventory_sha256") != ledger.get("inventory_sha256"):
        raise SystemExit("BLOCKED: inventory SHA-256 mismatch.")
    if sha256_file(args.ledger) != inventory.get("target_ledger_sha256"):
        raise SystemExit("BLOCKED: source ledger SHA-256 mismatch.")

    records = ledger.get("records")
    expected_count = target.get("occurrence_count")
    if not isinstance(records, list) or len(records) != expected_count:
        raise SystemExit("BLOCKED: target occurrence count mismatch.")
    if ledger.get("occurrence_count") != expected_count:
        raise SystemExit("BLOCKED: ledger declared occurrence count mismatch.")

    ids = [row.get("occurrence_id") for row in records]
    if any(not isinstance(value, str) or not value for value in ids):
        raise SystemExit("BLOCKED: missing occurrence ID.")
    if len(ids) != len(set(ids)):
        raise SystemExit("BLOCKED: duplicate occurrence IDs.")

    for row in records:
        if row.get("manual_classification") != "UNKNOWN":
            raise SystemExit("BLOCKED: source classification is not UNKNOWN.")
        if row.get("status") != "OPEN":
            raise SystemExit("BLOCKED: source record is not OPEN.")
        if row.get("reviewer_disposition") != "PENDING":
            raise SystemExit("BLOCKED: source reviewer disposition is not PENDING.")

    if args.output.exists():
        raise SystemExit(
            f"BLOCKED: output directory already exists; remove or choose a new path: {args.output}"
        )
    args.output.mkdir(parents=True, exist_ok=False)

    ledger_sha = sha256_file(args.ledger)
    batch_register = {
        "schema": "HCM_TYPE1_ADJUDICATION_BATCH_SET_V1",
        "target_commit": target["commit"],
        "inventory_ref": target["ref"],
        "inventory_sha256": inventory["reference_inventory_sha256"],
        "source_ledger_sha256": ledger_sha,
        "source_inventory_workflow_run_id": inventory["workflow_run_id"],
        "source_inventory_artifact_id": inventory["artifact_id"],
        "source_inventory_workflow_definition_commit": inventory[
            "workflow_definition_commit"
        ],
        "batch_size": BATCH_SIZE,
        "expected_occurrences": expected_count,
        "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
        "authority": "NONE",
        "batches": [],
    }

    for start in range(0, len(ids), BATCH_SIZE):
        batch_ids = ids[start : start + BATCH_SIZE]
        number = start // BATCH_SIZE + 1
        canonical = ("\n".join(batch_ids) + "\n").encode("utf-8")
        batch = {
            "schema": "HCM_TYPE1_ADJUDICATION_BATCH_REGISTER_V3",
            "batch_id": f"BATCH_{number:03d}",
            "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
            "target_commit": target["commit"],
            "inventory_ref": target["ref"],
            "inventory_sha256": inventory["reference_inventory_sha256"],
            "source_ledger_sha256": ledger_sha,
            "source_inventory_workflow_run_id": inventory["workflow_run_id"],
            "count": len(batch_ids),
            "first_occurrence_id": batch_ids[0],
            "last_occurrence_id": batch_ids[-1],
            "canonical_id_sequence_sha256": hashlib.sha256(canonical).hexdigest(),
            "canonicalization": "UTF-8; one occurrence ID per line; final newline included",
            "occurrence_ids": batch_ids,
            "authority": "NONE",
            "protocol_freeze": "NOT_FROZEN",
            "formal_calibration_authorized": False,
            "confirmatory_execution_authorized": False,
            "claim_support": False,
            "promotion_authority": False,
        }
        filename = f"BATCH_{number:03d}.json"
        batch_path = args.output / filename
        batch_path.write_text(
            json.dumps(batch, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        batch_register["batches"].append(
            {
                "batch_id": batch["batch_id"],
                "file": filename,
                "count": len(batch_ids),
                "sha256": sha256_file(batch_path),
            }
        )

    if len(batch_register["batches"]) != 72:
        raise SystemExit("BLOCKED: expected exactly 72 batches.")
    (args.output / "BATCH_SET_REGISTER.json").write_text(
        json.dumps(batch_register, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("BATCH_SET_GENERATED")
    print("batches:", len(batch_register["batches"]))
    print("occurrences:", expected_count)
    print("inventory_sha256:", inventory["reference_inventory_sha256"])
    print("source_ledger_sha256:", ledger_sha)
    print("All records remain OPEN / UNKNOWN / PENDING; authority=NONE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
