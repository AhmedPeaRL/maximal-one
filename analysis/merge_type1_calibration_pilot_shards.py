from __future__ import annotations

import argparse
import json
from pathlib import Path

IDENTITY_RANGE_KEYS = {"start_index", "stop_index"}


def common_identity(identity: dict) -> dict:
    return {key: value for key, value in identity.items() if key not in IDENTITY_RANGE_KEYS}


def merge_payloads(payloads: list[dict], total_repetitions: int) -> dict:
    if not payloads:
        raise ValueError("At least one pilot shard artifact is required")
    first_identity = payloads[0].get("run_identity")
    if not isinstance(first_identity, dict):
        raise ValueError("Missing run_identity in a shard")
    expected_common = common_identity(first_identity)
    seen: dict[int, dict] = {}
    shard_ranges: list[tuple[int, int]] = []
    for payload in payloads:
        identity = payload.get("run_identity")
        if not isinstance(identity, dict) or common_identity(identity) != expected_common:
            raise ValueError("Shard identity mismatch (scenario/seed/code/matrix/commit/config)")
        start, stop = int(identity["start_index"]), int(identity["stop_index"])
        if start < 0 or stop > total_repetitions or start >= stop:
            raise ValueError("Invalid shard range")
        shard_ranges.append((start, stop))
        rows = payload.get("attempt_records", [])
        for row in rows:
            index = int(row["replicate_index"])
            if not start <= index < stop:
                raise ValueError("Replicate record falls outside declared shard range")
            if index in seen:
                raise ValueError(f"Overlapping replicate index: {index}")
            seen[index] = row
    sorted_ranges = sorted(shard_ranges)
    for previous, current in zip(sorted_ranges, sorted_ranges[1:]):
        if current[0] < previous[1]:
            raise ValueError("Declared shard ranges overlap")
    expected = set(range(total_repetitions))
    complete = set(seen) == expected
    return {
        "artifact_kind": "MERGED_EXPLORATORY_PILOT_ONLY_NOT_FORMAL_CALIBRATION",
        "status": "PILOT_COMPLETE_DIAGNOSTIC_ONLY" if complete else "PILOT_INCOMPLETE_OR_DIAGNOSTIC_ONLY",
        "common_run_identity": expected_common,
        "total_repetitions_expected": total_repetitions,
        "completed_indices": sorted(seen),
        "missing_indices": sorted(expected - set(seen)),
        "shard_ranges": sorted(set(shard_ranges)),
        "attempt_records": [seen[index] for index in sorted(seen)],
        "invalid_attempts": sum(row.get("status") != "VALID" for row in seen.values()),
        "formal_calibration_pass": False,
        "claim_support": False,
        "promotion_authority": False,
        "confirmatory_null_frozen": False,
        "interpretation": "Merged pilot shards are runtime/engineering diagnostics only; they are not formal Type-I calibration results.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge exploratory Type-I pilot shards only")
    parser.add_argument("--total-repetitions", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("shards", nargs="+", type=Path)
    args = parser.parse_args()
    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in args.shards]
    merged = merge_payloads(payloads, args.total_repetitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": merged["status"], "completed": len(merged["completed_indices"]), "missing": merged["missing_indices"], "output": str(args.output)}, indent=2))
    return 0 if merged["status"] == "PILOT_COMPLETE_DIAGNOSTIC_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
