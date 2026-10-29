from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from analysis.merge_type1_execution_shards import merge_shards
from analysis.type1_execution_artifacts import (
    manifest_path_for,
    write_artifact_with_manifest,
)


TOTAL = 4


def identity(start: int, stop: int) -> dict:
    return {
        "protocol": "HCM_TYPE1_CALIBRATION_V4_CANDIDATE",
        "scenario_id": "synthetic_artifact_loss_test",
        "scenario_coefficients": [0.45, -0.10],
        "sample_size": 3328,
        "dgp_burn_in": 2000,
        "surrogates_requested": 1000,
        "total_repetitions": TOTAL,
        "master_seed": 20261021,
        "seed_schedule_id": "test-seed-schedule-v1",
        "start_index": start,
        "stop_index": stop,
        "commit_sha": "engineering-test-only",
        "matrix_sha256": "a" * 64,
        "runner_sha256": "b" * 64,
        "endpoint_identity": "canonical_primary_alpha",
        "null_implementation_identity": "existing-null-implementation",
        "requirements_lock_sha256": "c" * 64,
        "python_version": "test-runtime",
        "platform_identity": "test-platform",
    }


def attempt(index: int, status: str = "VALID") -> dict:
    return {
        "replicate_index": index,
        "status": status,
        "reason": None if status == "VALID" else "injected-invalid-attempt",
        "requested_surrogates": 1000,
        "valid_surrogates": 1000 if status == "VALID" else 0,
        "p_value_mc_add_one": 0.5 if status == "VALID" else None,
    }


def create_shard(
    path: Path,
    start: int,
    stop: int,
    records: list[dict],
) -> Path:
    write_artifact_with_manifest(
        path,
        {
            "artifact_kind": "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY",
            "attempt_records": records,
        },
        identity(start, stop),
    )
    return path


class ArtifactLossAndDenominatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.output = self.root / "merged.json"

        self.first = create_shard(
            self.root / "first.json",
            0,
            2,
            [attempt(0), attempt(1)],
        )
        self.second = create_shard(
            self.root / "second.json",
            2,
            4,
            [attempt(2), attempt(3)],
        )

    def tearDown(self):
        self.temp.cleanup()

    def assert_no_merged_output(self):
        self.assertFalse(
            self.output.exists(),
            "A rejected merge must not create a successful output artifact",
        )
        self.assertFalse(
            manifest_path_for(self.output).exists(),
            "A rejected merge must not create an output manifest",
        )

    def test_missing_artifact_blocks_merge(self):
        self.second.unlink()

        with self.assertRaisesRegex(ValueError, "Missing artifact"):
            merge_shards(
                [self.first, self.second],
                TOTAL,
                self.output,
            )

        self.assert_no_merged_output()

    def test_missing_manifest_blocks_merge(self):
        manifest_path_for(self.second).unlink()

        with self.assertRaisesRegex(
            ValueError, "Missing artifact manifest"
        ):
            merge_shards(
                [self.first, self.second],
                TOTAL,
                self.output,
            )

        self.assert_no_merged_output()

    def test_corrupt_manifest_blocks_merge(self):
        manifest_path_for(self.second).write_bytes(b"{not-json")

        with self.assertRaisesRegex(
            ValueError, "Unreadable artifact manifest"
        ):
            merge_shards(
                [self.first, self.second],
                TOTAL,
                self.output,
            )

        self.assert_no_merged_output()

    def test_missing_attempt_cannot_reduce_requested_denominator(self):
        # The shard declares indices 0 and 1 but only index 0 exists.
        create_shard(
            self.first,
            0,
            2,
            [attempt(0)],
        )

        with self.assertRaisesRegex(ValueError, "Shard is incomplete"):
            merge_shards(
                [self.first, self.second],
                TOTAL,
                self.output,
            )

        self.assert_no_merged_output()

    def test_invalid_attempt_is_preserved_not_replaced(self):
        create_shard(
            self.first,
            0,
            2,
            [attempt(0), attempt(1, "INVALID")],
        )

        merged = merge_shards(
            [self.first, self.second],
            TOTAL,
            self.output,
        )

        self.assertEqual(
            merged["total_repetitions_expected"],
            TOTAL,
        )
        self.assertEqual(
            merged["completed_indices"],
            [0, 1, 2, 3],
        )
        self.assertEqual(
            merged["invalid_attempts"],
            1,
        )
        self.assertEqual(
            merged["status"],
            "ENGINEERING_FAILED_INVALID_ATTEMPTS",
        )
        self.assertFalse(merged["formal_calibration_pass"])
        self.assertFalse(merged["claim_support"])
        self.assertFalse(merged["promotion_authority"])
        self.assertFalse(merged["confirmatory_execution_authorized"])

        # The invalid record remains visible at its original index.
        self.assertEqual(
            merged["attempt_records"][1]["status"],
            "INVALID",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
