from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


MANIFEST_SCHEMA = "HCM_TYPE1_EXECUTION_MANIFEST_V1"
MANIFEST_SUFFIX = ".manifest.json"

REQUIRED_IDENTITY_FIELDS = {
    "protocol",
    "scenario_id",
    "scenario_coefficients",
    "sample_size",
    "dgp_burn_in",
    "surrogates_requested",
    "total_repetitions",
    "master_seed",
    "seed_schedule_id",
    "start_index",
    "stop_index",
    "commit_sha",
    "matrix_sha256",
    "runner_sha256",
    "endpoint_identity",
    "null_implementation_identity",
    "requirements_lock_sha256",
    "python_version",
    "platform_identity",
}


def canonical_json_bytes(value: Any) -> bytes:
    """Stable JSON serialization for identity and digest calculations."""
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """Write to a sibling temporary file, then atomically replace target."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary_name = stream.name
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())

        os.replace(temporary_name, path)
        temporary_name = None

    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass


def atomic_write_json(path: Path, payload: dict) -> None:
    atomic_write_bytes(path, canonical_json_bytes(payload))


def validate_run_identity(identity: dict) -> None:
    if not isinstance(identity, dict):
        raise ValueError("run_identity must be a JSON object")

    missing = sorted(REQUIRED_IDENTITY_FIELDS - set(identity))
    if missing:
        raise ValueError(
            "Missing required run identity fields: "
            + ", ".join(missing)
        )

    for field in REQUIRED_IDENTITY_FIELDS:
        value = identity[field]

        if value is None:
            raise ValueError(
                f"Run identity field cannot be null: {field}"
            )

        if isinstance(value, str) and not value.strip():
            raise ValueError(
                f"Run identity field cannot be empty: {field}"
            )

    start = identity["start_index"]
    stop = identity["stop_index"]
    total = identity["total_repetitions"]

    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in (start, stop, total)
    ):
        raise ValueError(
            "Shard indices and total repetitions must be integers"
        )

    if total < 1 or start < 0 or stop > total or start >= stop:
        raise ValueError(
            "Require 0 <= start_index < stop_index <= total_repetitions"
        )

    for field in (
        "matrix_sha256",
        "runner_sha256",
        "requirements_lock_sha256",
    ):
        value = identity[field]

        if (
            not isinstance(value, str)
            or len(value) != 64
            or any(c not in "0123456789abcdef" for c in value.lower())
        ):
            raise ValueError(
                f"Malformed SHA-256 identity field: {field}"
            )


def manifest_path_for(artifact_path: Path) -> Path:
    return Path(str(artifact_path) + MANIFEST_SUFFIX)


def write_artifact_with_manifest(
    artifact_path: Path,
    payload: dict,
    run_identity: dict,
) -> dict:
    """
    Write a payload and its integrity manifest.

    If the process stops between the two writes, verification fails closed:
    the artifact is not accepted without its matching manifest.
    """
    validate_run_identity(run_identity)

    if not isinstance(payload, dict):
        raise ValueError("Artifact payload must be a JSON object")

    artifact = dict(payload)
    artifact["run_identity"] = run_identity

    artifact_bytes = canonical_json_bytes(artifact)
    artifact_path = Path(artifact_path)

    atomic_write_bytes(artifact_path, artifact_bytes)
    artifact_hash = sha256_file(artifact_path)

    manifest = {
        "manifest_schema": MANIFEST_SCHEMA,
        "artifact_file": artifact_path.name,
        "artifact_sha256": artifact_hash,
        "run_identity": run_identity,
    }

    atomic_write_json(manifest_path_for(artifact_path), manifest)

    return {
        "artifact_path": str(artifact_path),
        "manifest_path": str(manifest_path_for(artifact_path)),
        "artifact_sha256": artifact_hash,
    }


def load_verified_artifact(
    artifact_path: Path,
    expected_identity: dict | None = None,
) -> dict:
    """Verify the manifest, file hash, and identity before returning data."""
    artifact_path = Path(artifact_path)
    manifest_path = manifest_path_for(artifact_path)

    if not artifact_path.is_file():
        raise ValueError(f"Missing artifact: {artifact_path}")

    if not manifest_path.is_file():
        raise ValueError(f"Missing artifact manifest: {manifest_path}")

    try:
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        raise ValueError(
            f"Unreadable artifact manifest: {manifest_path}"
        ) from exc

    if manifest.get("manifest_schema") != MANIFEST_SCHEMA:
        raise ValueError("Unsupported execution manifest schema")

    if manifest.get("artifact_file") != artifact_path.name:
        raise ValueError("Manifest artifact filename mismatch")

    expected_hash = manifest.get("artifact_sha256")
    if (
        not isinstance(expected_hash, str)
        or len(expected_hash) != 64
    ):
        raise ValueError("Missing or malformed manifest SHA-256")

    actual_hash = sha256_file(artifact_path)
    if actual_hash.lower() != expected_hash.lower():
        raise ValueError("Artifact SHA-256 mismatch")

    try:
        payload = json.loads(
            artifact_path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        raise ValueError(
            f"Unreadable artifact JSON: {artifact_path}"
        ) from exc

    artifact_identity = payload.get("run_identity")
    manifest_identity = manifest.get("run_identity")

    validate_run_identity(artifact_identity)
    validate_run_identity(manifest_identity)

    if artifact_identity != manifest_identity:
        raise ValueError("Manifest/artifact run identity mismatch")

    if (
        expected_identity is not None
        and artifact_identity != expected_identity
    ):
        raise ValueError(
            "Artifact run identity differs from requested execution"
        )

    payload["_verified_artifact_sha256"] = actual_hash
    return payload


def validate_attempt_records(
    records: list,
    start_index: int,
    stop_index: int,
) -> dict:
    """Validate indices and preserve invalid attempts rather than dropping them."""
    if not isinstance(records, list):
        raise ValueError("attempt_records must be a list")

    seen = set()

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Malformed attempt record")

        index = record.get("replicate_index")

        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("replicate_index must be an integer")

        if not start_index <= index < stop_index:
            raise ValueError(
                f"Replicate index outside requested range: {index}"
            )

        if index in seen:
            raise ValueError(
                f"Duplicate replicate index: {index}"
            )

        if record.get("status") not in {"VALID", "INVALID"}:
            raise ValueError(
                f"Invalid attempt status at replicate {index}"
            )

        seen.add(index)

    expected = set(range(start_index, stop_index))
    observed = seen

    return {
        "expected_count": len(expected),
        "observed_count": len(observed),
        "missing_indices": sorted(expected - observed),
        "complete": observed == expected,
        "invalid_count": sum(
            row["status"] == "INVALID" for row in records
        ),
    }
