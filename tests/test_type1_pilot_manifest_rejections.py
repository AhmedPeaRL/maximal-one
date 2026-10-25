from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from analysis.merge_type1_calibration_pilot_shards import (
    load_verified_shard,
    manifest_path_for,
)


def write_test_artifact(directory: Path) -> Path:
    identity = {
        "scenario": "manifest_rejection_test",
        "master_seed": 20261021,
        "commit_sha": "engineering-test-only",
        "matrix_sha256": "matrix-test-hash",
        "runner_sha256": "runner-test-hash",
        "surrogates": 200,
        "start_index": 0,
        "stop_index": 1,
    }

    payload = {
        "run_identity": identity,
        "attempt_records": [
            {
                "replicate_index": 0,
                "status": "VALID",
            }
        ],
    }

    artifact = directory / "shard.json"
    artifact.write_text(
        json.dumps(payload, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    manifest = {
        "manifest_schema": "HCM_TYPE1_PILOT_ARTIFACT_MANIFEST_V1",
        "artifact_file": artifact.name,
        "artifact_sha256": digest,
        "run_identity": identity,
    }

    manifest_path_for(artifact).write_text(
        json.dumps(manifest, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return artifact


class PilotManifestRejectionTests(unittest.TestCase):
    """Manifest integrity tests; not formal Type-I calibration."""

    def test_manifest_run_identity_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            artifact = write_test_artifact(directory)
            manifest_path = manifest_path_for(artifact)

            manifest = json.loads(
                manifest_path.read_text(encoding="utf-8")
            )
            manifest["run_identity"]["scenario"] = "different_scenario"

            # The artifact hash remains valid. Only the manifest identity
            # is changed, so the identity check itself must reject the input.
            manifest_path.write_text(
                json.dumps(manifest, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, "Manifest/run identity mismatch"
            ):
                load_verified_shard(artifact)

    def test_artifact_hash_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            artifact = write_test_artifact(directory)

            # Modify the artifact after the manifest records its hash.
            artifact.write_text(
                artifact.read_text(encoding="utf-8") + "tampered\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, "SHA-256 mismatch for shard"
            ):
                load_verified_shard(artifact)


if __name__ == "__main__":
    unittest.main(verbosity=2)
