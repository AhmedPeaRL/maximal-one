from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from analysis.type1_execution_artifacts import (
    atomic_write_json,
    load_verified_artifact,
    manifest_path_for,
    validate_attempt_records,
    write_artifact_with_manifest,
)


def test_identity():
    return {
        "protocol": "ENGINEERING_TEST_ONLY",
        "scenario_id": "synthetic_test",
        "scenario_coefficients": [0.4],
        "sample_size": 3328,
        "dgp_burn_in": 2000,
        "surrogates_requested": 1000,
        "total_repetitions": 2,
        "master_seed": 20261021,
        "seed_schedule_id": "test-seed-schedule-v1",
        "start_index": 0,
        "stop_index": 2,
        "commit_sha": "engineering-test-only",
        "matrix_sha256": "a" * 64,
        "runner_sha256": "b" * 64,
        "endpoint_identity": "canonical_primary_alpha",
        "null_implementation_identity": "existing-null-implementation",
        "requirements_lock_sha256": "c" * 64,
        "python_version": "test-runtime",
        "platform_identity": "test-platform",
    }


class ExecutionArtifactTests(unittest.TestCase):

    def test_round_trip_verifies_artifact_and_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "shard.json"
            identity = test_identity()

            write_artifact_with_manifest(
                path,
                {"attempt_records": []},
                identity,
            )

            loaded = load_verified_artifact(
                path,
                expected_identity=identity,
            )

            self.assertEqual(
                loaded["run_identity"],
                identity,
            )
            self.assertTrue(
                Path(manifest_path_for(path)).is_file()
            )

    def test_missing_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "shard.json"
            path.write_text(
                json.dumps({"run_identity": test_identity()}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, "Missing artifact manifest"
            ):
                load_verified_artifact(path)

    def test_artifact_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "shard.json"

            write_artifact_with_manifest(
                path,
                {"attempt_records": []},
                test_identity(),
            )

            path.write_text(
                path.read_text(encoding="utf-8") + "tampered\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, "Artifact SHA-256 mismatch"
            ):
                load_verified_artifact(path)

    def test_resume_identity_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "checkpoint.json"
            identity = test_identity()

            write_artifact_with_manifest(
                path,
                {"attempt_records": []},
                identity,
            )

            different_identity = dict(identity)
            different_identity["master_seed"] += 1

            with self.assertRaisesRegex(
                ValueError, "differs from requested execution"
            ):
                load_verified_artifact(
                    path,
                    expected_identity=different_identity,
                )

    def test_duplicate_replicate_index_is_rejected(self):
        records = [
            {"replicate_index": 0, "status": "VALID"},
            {"replicate_index": 0, "status": "VALID"},
        ]

        with self.assertRaisesRegex(
            ValueError, "Duplicate replicate index"
        ):
            validate_attempt_records(records, 0, 2)

    def test_out_of_range_replicate_is_rejected(self):
        records = [
            {"replicate_index": 2, "status": "VALID"},
        ]

        with self.assertRaisesRegex(
            ValueError, "outside requested range"
        ):
            validate_attempt_records(records, 0, 2)

    def test_missing_attempt_is_reported_not_hidden(self):
        result = validate_attempt_records(
            [
                {"replicate_index": 0, "status": "VALID"},
                {"replicate_index": 2, "status": "INVALID"},
            ],
            0,
            3,
        )

        self.assertFalse(result["complete"])
        self.assertEqual(result["missing_indices"], [1])
        self.assertEqual(result["invalid_count"], 1)

    def test_invalid_attempt_is_not_a_success(self):
        result = validate_attempt_records(
            [
                {"replicate_index": 0, "status": "VALID"},
                {"replicate_index": 1, "status": "INVALID"},
            ],
            0,
            2,
        )

        self.assertTrue(result["complete"])
        self.assertEqual(result["invalid_count"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
