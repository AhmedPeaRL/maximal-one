from __future__ import annotations

import argparse
import json
from pathlib import Path

from analysis.type1_execution_artifacts import (
    load_verified_artifact,
    validate_attempt_records,
    write_artifact_with_manifest,
)

RANGE_KEYS = {"start_index", "stop_index"}


def common_identity(identity: dict) -> dict:
    return {key: value for key, value in identity.items() if key not in RANGE_KEYS}


def merge_shards(shard_paths: list[Path], total_repetitions: int, output: Path) -> dict:
    if total_repetitions < 1:
        raise ValueError("total_repetitions must be positive")
    if not shard_paths:
        raise ValueError("At least one verified shard is required")

    loaded = []
    for path in shard_paths:
        payload = load_verified_artifact(path)
        if payload.get("artifact_kind") != "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY":
            raise ValueError(f"Not an official-runner engineering artifact: {path}")
        identity = payload.get("run_identity")
        if not isinstance(identity, dict):
            raise ValueError(f"Missing run identity: {path}")
        if identity.get("total_repetitions") != total_repetitions:
            raise ValueError("Shard total_repetitions mismatch")
        validation = validate_attempt_records(
            payload.get("attempt_records"), identity["start_index"], identity["stop_index"]
        )
        if not validation["complete"]:
            raise ValueError(f"Shard is incomplete; missing {validation['missing_indices']}: {path}")
        loaded.append((path, payload, identity, validation))

    base_identity = common_identity(loaded[0][2])
    seen = {}
    ranges = []
    shard_hashes = []
    for path, payload, identity, validation in loaded:
        if common_identity(identity) != base_identity:
            raise ValueError("Shard common run identity mismatch")
        start, stop = identity["start_index"], identity["stop_index"]
        if start < 0 or stop > total_repetitions or start >= stop:
            raise ValueError("Invalid declared shard range")
        ranges.append((start, stop))
        for row in payload["attempt_records"]:
            index = row["replicate_index"]
            if not start <= index < stop:
                raise ValueError(f"Replicate {index} is outside declared shard range")
            if index in seen:
                raise ValueError(f"Duplicate/overlapping replicate index: {index}")
            seen[index] = row
        shard_hashes.append({
            "artifact": path.name,
            "sha256": payload.get("_verified_artifact_sha256"),
        })

    ordered_ranges = sorted(ranges)
    cursor = 0
    for start, stop in ordered_ranges:
        if start != cursor:
            raise ValueError(f"Shard ranges have a gap or overlap at index {cursor}")
        cursor = stop
    if cursor != total_repetitions:
        raise ValueError(f"Shard ranges cover 0..{cursor}, not 0..{total_repetitions}")
    expected = set(range(total_repetitions))
    if set(seen) != expected:
        raise ValueError(f"Merged indices differ from requested denominator; missing={sorted(expected - set(seen))}")

    records = [seen[i] for i in range(total_repetitions)]
    invalid = sum(row.get("status") != "VALID" for row in records)
    merged_identity = dict(base_identity)
    merged_identity["start_index"] = 0
    merged_identity["stop_index"] = total_repetitions
    merged = {
        "artifact_kind": "V4_OFFICIAL_RUNNER_ENGINEERING_MERGE_ONLY",
        "status": "ENGINEERING_FAILED_INVALID_ATTEMPTS" if invalid else "ENGINEERING_COMPLETE",
        "total_repetitions_expected": total_repetitions,
        "completed_indices": list(range(total_repetitions)),
        "missing_indices": [],
        "invalid_attempts": invalid,
        "attempt_records": records,
        "shard_ranges": [list(pair) for pair in ordered_ranges],
        "verified_shard_hashes": sorted(shard_hashes, key=lambda row: (row["sha256"] or "", row["artifact"])),
        "formal_calibration_pass": False,
        "claim_support": False,
        "promotion_authority": False,
        "confirmatory_execution_authorized": False,
        "confirmatory_null_frozen": False,
        "interpretation": "Integrity-verified engineering merge only; not a formal calibration result.",
    }
    write_artifact_with_manifest(output, merged, merged_identity)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge integrity-verified official-runner engineering shards only.")
    parser.add_argument("--total-repetitions", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("shards", nargs="+", type=Path)
    args = parser.parse_args()
    result = merge_shards(args.shards, args.total_repetitions, args.output)
    print(json.dumps({"status": result["status"], "completed": len(result["completed_indices"]), "invalid_attempts": result["invalid_attempts"], "output": str(args.output), "formal_calibration_pass": False}, indent=2))
    # A complete merge can still report invalid scientific attempts. This exit
    # code reports structural integrity, not scientific success.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
