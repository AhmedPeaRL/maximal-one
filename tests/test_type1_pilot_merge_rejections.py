from __future__ import annotations

import unittest

from analysis.merge_type1_calibration_pilot_shards import merge_payloads


def make_shard(start, stop, indices, *, scenario="test_scenario"):
    return {
        "run_identity": {
            "scenario": scenario,
            "master_seed": 20261021,
            "commit_sha": "engineering-test-only",
            "matrix_sha256": "matrix-test-hash",
            "runner_sha256": "runner-test-hash",
            "surrogates": 200,
            "start_index": start,
            "stop_index": stop,
        },
        "attempt_records": [
            {
                "replicate_index": index,
                "status": "VALID",
            }
            for index in indices
        ],
    }


class PilotMergeRejectionTests(unittest.TestCase):
    """Unit tests for rejection and incompleteness in the pilot merger.

    These tests do not execute or authorize formal Type-I calibration.
    """

    def test_duplicate_index_inside_one_shard_is_rejected(self):
        shard = make_shard(0, 2, [0, 0])

        with self.assertRaisesRegex(
            ValueError, "Duplicate replicate index inside shard"
        ):
            merge_payloads([shard], total_repetitions=2)

    def test_overlapping_declared_ranges_are_rejected(self):
        shard_a = make_shard(0, 2, [0])
        shard_b = make_shard(1, 3, [2])

        with self.assertRaisesRegex(
            ValueError, "Declared shard ranges overlap"
        ):
            merge_payloads([shard_a, shard_b], total_repetitions=3)

    def test_duplicate_index_across_shards_is_rejected(self):
        shard_a = make_shard(0, 2, [0, 1])
        shard_b = make_shard(1, 3, [1, 2])

        with self.assertRaisesRegex(
            ValueError, "Overlapping replicate index"
        ):
            merge_payloads([shard_a, shard_b], total_repetitions=3)

    def test_missing_indices_cannot_report_completion(self):
        shard_a = make_shard(0, 2, [0])
        shard_b = make_shard(2, 4, [2, 3])

        merged = merge_payloads(
            [shard_a, shard_b],
            total_repetitions=4,
        )

        self.assertEqual(
            merged["status"],
            "PILOT_INCOMPLETE_OR_DIAGNOSTIC_ONLY",
        )
        self.assertEqual(merged["missing_indices"], [1])
        self.assertFalse(merged["formal_calibration_pass"])
        self.assertFalse(merged["claim_support"])
        self.assertFalse(merged["promotion_authority"])

    def test_common_run_identity_mismatch_is_rejected(self):
        shard_a = make_shard(0, 2, [0])
        shard_b = make_shard(2, 4, [2, 3], scenario="different_scenario")

        with self.assertRaisesRegex(
            ValueError, "Shard identity mismatch"
        ):
            merge_payloads([shard_a, shard_b], total_repetitions=4)

    def test_invalid_attempt_prevents_pilot_completion_pass(self):
        shard = make_shard(0, 2, [0, 1])
        shard["attempt_records"][1]["status"] = "INVALID"

        merged = merge_payloads([shard], total_repetitions=2)

        self.assertEqual(
            merged["status"],
            "PILOT_FAILED_DIAGNOSTIC_ONLY",
        )
        self.assertEqual(merged["invalid_attempts"], 1)
        self.assertFalse(merged["formal_calibration_pass"])
        self.assertFalse(merged["claim_support"])
        self.assertFalse(merged["promotion_authority"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
