from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

BATCH_SIZE = 25
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"BLOCKED: expected JSON object: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"BLOCKED: {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--population-register", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--artifact-metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    population = read_json(args.population_register)
    ledger = read_json(args.ledger)
    provenance = read_json(args.provenance)
    artifact = read_json(args.artifact_metadata)
    target = population["target"]
    main = population["main_comparison"]
    inv = population["inventory"]

    # Validate the population register's own source identity fields.
    require(target.get("commit") == ledger.get("inventory_commit"), "target commit mismatch")
    require(target.get("ref") == ledger.get("inventory_ref"), "inventory ref mismatch")
    require(target.get("occurrence_count") == 1800, "population target count is not 1800")
    require(main.get("occurrence_count") == 728, "current main population count is not 728")
    require(COMMIT_RE.fullmatch(str(target.get("commit", ""))) is not None, "invalid target commit")
    require(COMMIT_RE.fullmatch(str(main.get("commit", ""))) is not None, "invalid main commit")

    # Compare register values against downloaded artifact provenance and live GitHub metadata.
    require(str(inv.get("workflow_run_id")) == str(provenance.get("workflow_run_id")), "inventory workflow run ID mismatch")
    require(str(inv.get("artifact_id")) == str(artifact.get("id")), "inventory artifact ID mismatch")
    require(inv.get("artifact_name") == artifact.get("name"), "inventory artifact name mismatch")
    require(inv.get("artifact_archive_sha256") == str(artifact.get("digest", "")).removeprefix("sha256:"), "inventory artifact digest mismatch")
    require(str(artifact.get("workflow_run", {}).get("id")) == str(inv.get("workflow_run_id")), "artifact workflow run ID mismatch")
    require(provenance.get("target_commit") == target.get("commit"), "provenance target commit mismatch")
    require(provenance.get("main_commit") == main.get("commit"), "provenance main commit mismatch")
    require(provenance.get("workflow_definition_commit") == inv.get("workflow_definition_commit"), "workflow-definition commit mismatch")
    require(provenance.get("inventory_sha256") == inv.get("reference_inventory_sha256"), "provenance inventory SHA mismatch")

    require(artifact.get("expired") is False, "inventory artifact is expired or expiry is unknown")
    for field in ("reference_inventory_sha256", "target_ledger_sha256", "main_ledger_sha256", "artifact_archive_sha256"):
        require(SHA256_RE.fullmatch(str(inv.get(field, ""))) is not None, f"invalid {field}")
    require(COMMIT_RE.fullmatch(str(inv.get("workflow_definition_commit", ""))) is not None, "invalid workflow-definition commit")

    require(sha256_file(args.inventory) == inv["reference_inventory_sha256"], "inventory SHA-256 mismatch")
    require(sha256_file(args.ledger) == inv["target_ledger_sha256"], "source ledger SHA-256 mismatch")
    main_ledger_path = args.ledger.parent / "main_occurrence_level_manual_ledger.json"
    require(main_ledger_path.is_file(), "main comparison ledger is missing")
    require(sha256_file(main_ledger_path) == inv["main_ledger_sha256"], "main ledger SHA-256 mismatch")
    require(ledger.get("inventory_sha256") == inv["reference_inventory_sha256"], "ledger inventory SHA-256 mismatch")

    records = ledger.get("records")
    expected_count = target.get("occurrence_count")
    require(isinstance(records, list) and len(records) == expected_count, "target occurrence count mismatch")
    require(ledger.get("occurrence_count") == expected_count, "ledger declared occurrence count mismatch")
    ids = [row.get("occurrence_id") for row in records]
    require(all(isinstance(value, str) and value for value in ids), "missing occurrence ID")
    require(len(ids) == len(set(ids)), "duplicate occurrence IDs")
    for row in records:
        require(row.get("manual_classification") == "UNKNOWN", "source classification is not UNKNOWN")
        require(row.get("status") == "OPEN", "source record is not OPEN")
        require(row.get("reviewer_disposition") == "PENDING", "source reviewer disposition is not PENDING")

    require(not args.output.exists(), f"output directory already exists: {args.output}")
    args.output.mkdir(parents=True, exist_ok=False)
    ledger_sha = sha256_file(args.ledger)
    register = {
        "schema": "HCM_TYPE1_ADJUDICATION_BATCH_SET_V2",
        "target_commit": target["commit"],
        "main_commit": main["commit"],
        "inventory_ref": target["ref"],
        "inventory_sha256": inv["reference_inventory_sha256"],
        "source_ledger_sha256": ledger_sha,
        "source_main_ledger_sha256": inv["main_ledger_sha256"],
        "source_inventory_workflow_run_id": str(inv["workflow_run_id"]),
        "source_inventory_artifact_id": str(inv["artifact_id"]),
        "source_inventory_artifact_name": inv["artifact_name"],
        "source_inventory_artifact_archive_sha256": inv["artifact_archive_sha256"],
        "source_inventory_workflow_definition_commit": inv["workflow_definition_commit"],
        "batch_size": BATCH_SIZE,
        "expected_occurrences": expected_count,
        "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
        "authority": "NONE",
        "batches": [],
    }

    for start in range(0, len(ids), BATCH_SIZE):
        batch_ids = ids[start:start + BATCH_SIZE]
        number = start // BATCH_SIZE + 1
        canonical = ("\n".join(batch_ids) + "\n").encode("utf-8")
        batch = {
            "schema": "HCM_TYPE1_ADJUDICATION_BATCH_V2",
            "batch_id": f"BATCH_{number:03d}",
            "status": "NAVIGATION_ONLY_NOT_ADJUDICATED",
            "target_commit": target["commit"],
            "main_commit": main["commit"],
            "inventory_ref": target["ref"],
            "inventory_sha256": inv["reference_inventory_sha256"],
            "source_ledger_sha256": ledger_sha,
            "source_inventory_workflow_run_id": str(inv["workflow_run_id"]),
            "source_inventory_artifact_id": str(inv["artifact_id"]),
            "source_inventory_workflow_definition_commit": inv["workflow_definition_commit"],
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
        batch_path.write_text(json.dumps(batch, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        register["batches"].append({
            "batch_id": batch["batch_id"],
            "file": filename,
            "count": len(batch_ids),
            "sha256": sha256_file(batch_path),
        })

    require(len(register["batches"]) == 72, "expected exactly 72 batches")
    (args.output / "BATCH_SET_REGISTER.json").write_text(json.dumps(register, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("BATCH_SET_GENERATED_AND_SOURCE_BOUND")
    print("batches:", len(register["batches"]))
    print("occurrences:", expected_count)
    print("inventory_run_id:", inv["workflow_run_id"])
    print("inventory_artifact_id:", inv["artifact_id"])
    print("inventory_sha256:", inv["reference_inventory_sha256"])
    print("source_ledger_sha256:", ledger_sha)
    print("All records remain OPEN / UNKNOWN / PENDING; authority=NONE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
