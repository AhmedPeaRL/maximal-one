import hashlib
import json
from pathlib import Path

SOURCE = Path(
    "evidence/occurrence_level_manual_ledger.json"
)
OUT = Path("adjudication/target_1800_batches")
BATCH_SIZE = 25

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

ledger = json.loads(SOURCE.read_text(encoding="utf-8"))

assert ledger["inventory_commit"] == (
    "ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876"
)
assert ledger["inventory_sha256"] == (
    "88222e3178bc62854ffb8d1fa961c1fb4cfe582c9ff1082878ab759e011cc635"
)
assert ledger["occurrence_count"] == 1800
assert len(ledger["records"]) == 1800

ids = [r["occurrence_id"] for r in ledger["records"]]
assert len(ids) == len(set(ids))

for row in ledger["records"]:
    assert row["manual_classification"] == "UNKNOWN"
    assert row["status"] == "OPEN"
    assert row["reviewer_disposition"] == "PENDING"

OUT.mkdir(parents=True, exist_ok=True)

register = {
    "schema": "HCM_TYPE1_ADJUDICATION_BATCH_SET_V1",
    "target_commit": ledger["inventory_commit"],
    "inventory_ref": ledger["inventory_ref"],
    "inventory_sha256": ledger["inventory_sha256"],
    "source_ledger_sha256": sha256(SOURCE.read_bytes()),
    "batch_size": BATCH_SIZE,
    "expected_occurrences": len(ids),
    "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
    "authority": "NONE",
    "batches": []
}

for start in range(0, len(ids), BATCH_SIZE):
    batch_ids = ids[start:start + BATCH_SIZE]
    batch_number = start // BATCH_SIZE + 1
    canonical = ("\n".join(batch_ids) + "\n").encode("utf-8")

    batch = {
        "schema": "HCM_TYPE1_ADJUDICATION_BATCH_REGISTER_V3",
        "batch_id": f"BATCH_{batch_number:03d}",
        "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
        "target_commit": ledger["inventory_commit"],
        "inventory_ref": ledger["inventory_ref"],
        "inventory_sha256": ledger["inventory_sha256"],
        "source_ledger_sha256": register["source_ledger_sha256"],
        "count": len(batch_ids),
        "first_occurrence_id": batch_ids[0],
        "last_occurrence_id": batch_ids[-1],
        "canonical_id_sequence_sha256": sha256(canonical),
        "canonicalization": (
            "UTF-8; one occurrence ID per line; final newline included"
        ),
        "occurrence_ids": batch_ids,
        "authority": "NONE",
        "protocol_freeze": "NOT_FROZEN",
        "formal_calibration_authorized": False,
        "confirmatory_execution_authorized": False,
        "claim_support": False,
        "promotion_authority": False
    }

    name = f"BATCH_{batch_number:03d}.json"
    (OUT / name).write_text(
        json.dumps(batch, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    register["batches"].append({
        "batch_id": batch["batch_id"],
        "file": name,
        "count": len(batch_ids),
        "sha256": sha256(
            (OUT / name).read_bytes()
        )
    })

assert sum(x["count"] for x in register["batches"]) == 1800
assert len(register["batches"]) == 72

(OUT / "BATCH_SET_REGISTER.json").write_text(
    json.dumps(register, indent=2, sort_keys=True) + "\n",
    encoding="utf-8"
)

print("BATCH_SET_GENERATED")
print("batches:", len(register["batches"]))
print("occurrences:", sum(x["count"] for x in register["batches"]))
print("inventory_sha256:", ledger["inventory_sha256"])
print("All records remain OPEN / UNKNOWN / PENDING.")
