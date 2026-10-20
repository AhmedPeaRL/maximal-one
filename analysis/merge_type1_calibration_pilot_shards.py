from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

IDENTITY_RANGE_KEYS = {"start_index", "stop_index"}
MANIFEST_SUFFIX = ".manifest.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def common_identity(identity: dict) -> dict:
    return {
        key: value
        for key, value in identity.items()
        if key not in IDENTITY_RANGE_KEYS
    }


def manifest_path_for(artifact_path: Path) -> Path:
    return Path(str(artifact_path) + MANIFEST_SUFFIX)


def load_verified_shard(artifact_path: Path) -> dict:
    """Load a shard only after checking its separate SHA-256 manifest."""
    manifest_path = manifest_path_for(artifact_path)

    if not artifact_path.is_file():
        raise ValueError(f"Missing shard artifact: {artifact_path}")
    if not manifest_path.is_file():
        raise ValueError(f"Missing shard manifest: {manifest_path}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(
            f"Unreadable shard manifest: {manifest_path}: {exc}"
        ) from exc

    expected_hash = manifest.get("artifact_sha256")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ValueError(
            f"Missing or malformed artifact_sha256: {manifest_path}"
        )

    actual_hash = sha256_file(artifact_path)
    if actual_hash.lower() != expected_hash.lower():
        raise ValueError(
            f"SHA-256 mismatch for shard: {artifact_path}"
        )

    if manifest.get("artifact_file") != artifact_path.name:
        raise ValueError(
            f"Manifest artifact filename mismatch: {manifest_path}"
        )

    try:
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(
            f"Unreadable shard artifact: {artifact_path}: {exc}"
        ) from exc

    artifact_identity = payload.get("run_identity")
    manifest_identity = manifest.get("run_identity")

    if not isinstance(artifact_identity, dict):
        raise ValueError(f"Missing run_identity: {artifact_path}")
    if not isinstance(manifest_identity, dict):
        raise ValueError(f"Missing run_identity in manifest: {manifest_path}")
    if artifact_identity != manifest_identity:
        raise ValueError(
            f"Manifest/run identity mismatch: {artifact_path}"
        )

    payload["_verified_artifact_sha256"] = actual_hash
    payload["_verified_manifest_path"] = str(manifest_path)
    return payload


def merge_payloads(
    payloads: list[dict],
    total_repetitions: int,
) -> dict:
    if total_repetitions < 1:
        raise ValueError("total_repetitions must be positive")
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
        if (
            not isinstance(identity, dict)
            or common_identity(identity) != expected_common
        ):
            raise ValueError(
                "Shard identity mismatch "
                "(scenario/seed/code/matrix/commit/config)"
            )

        try:
            start = int(identity["start_index"])
            stop = int(identity["stop_index"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Missing or invalid shard range") from exc

        if start < 0 or stop > total_repetitions or start >= stop:
            raise ValueError("Invalid shard range")

        shard_ranges.append((start, stop))
        rows = payload.get("attempt_records")

        if not isinstance(rows, list):
            raise ValueError("attempt_records must be a list")

        indices_in_shard: set[int] = set()

        for row in rows:
            if not isinstance(row, dict) or "replicate_index" not in row:
                raise ValueError("Malformed attempt record")

            index = int(row["replicate_index"])

            if not start <= index < stop:
                raise ValueError(
                    "Replicate record falls outside declared shard range"
                )
            if index in indices_in_shard:
                raise ValueError(
                    f"Duplicate replicate index inside shard: {index}"
                )
            if index in seen:
                raise ValueError(f"Overlapping replicate index: {index}")

            indices_in_shard.add(index)
            seen[index] = row

    sorted_ranges = sorted(shard_ranges)
    for previous, current in zip(sorted_ranges, sorted_ranges[1:]):
        if current[0] < previous[1]:
            raise ValueError("Declared shard ranges overlap")

    expected = set(range(total_repetitions))
    observed = set(seen)
    complete = observed == expected
    invalid_count = sum(
        row.get("status") != "VALID" for row in seen.values()
    )

    return {
        "artifact_kind":
            "MERGED_EXPLORATORY_PILOT_ONLY_NOT_FORMAL_CALIBRATION",
        "status": (
            "PILOT_COMPLETE_DIAGNOSTIC_ONLY"
            if complete
            else "PILOT_INCOMPLETE_OR_DIAGNOSTIC_ONLY"
        ),
        "common_run_identity": expected_common,
        "total_repetitions_expected": total_repetitions,
        "completed_indices": sorted(observed),
        "missing_indices": sorted(expected - observed),
        "shard_ranges": [list(item) for item in sorted(set(shard_ranges))],
        "attempt_records": [seen[index] for index in sorted(seen)],
        "invalid_attempts": invalid_count,
        "verified_shard_hashes": [
            {
                "sha256": payload.get("_verified_artifact_sha256"),
                "manifest": payload.get("_verified_manifest_path"),
            }
            for payload in payloads
        ],
        "formal_calibration_pass": False,
        "claim_support": False,
        "promotion_authority": False,
        "confirmatory_null_frozen": False,
        "interpretation":
            "Merged pilot shards are engineering diagnostics only. "
            "Every input artifact must pass separate-manifest SHA-256 "
            "verification before it can be merged.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge verified exploratory Type-I pilot shards only"
    )
    parser.add_argument("--total-repetitions", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("shards", nargs="+", type=Path)
    args = parser.parse_args()

    # Verify every artifact before passing any payload to the merger.
    payloads = [load_verified_shard(path) for path in args.shards]
    merged = merge_payloads(payloads, args.total_repetitions)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(merged, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": merged["status"],
                "completed": len(merged["completed_indices"]),
                "missing": merged["missing_indices"],
                "invalid_attempts": merged["invalid_attempts"],
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return (
        0
        if merged["status"] == "PILOT_COMPLETE_DIAGNOSTIC_ONLY"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
