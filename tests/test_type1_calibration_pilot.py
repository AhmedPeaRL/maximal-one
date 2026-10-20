from __future__ import annotations

import unittest

import numpy as np

from analysis.type1_calibration_pilot import (
    MATRIX,
    SCENARIOS,
    replicate_rngs,
    shard_indices,
    stable_scenario_key,
)
from analysis.merge_type1_calibration_pilot_shards import merge_payloads


class TypeICalibrationPilotTests(unittest.TestCase):
    def test_pilot_matrix_is_not_frozen_or_confirmatory(self):
        self.assertEqual(MATRIX["status"], "DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW")
        self.assertEqual(MATRIX["freeze_state"], "NOT_FROZEN")
        self.assertFalse(MATRIX["confirmatory_execution_authorized"])

    def test_in_band_resonance_scenarios_are_inside_declared_band(self):
        band_low, band_high = MATRIX["primary_design_candidate"]["frequency_band_open_interval"]
        rows = {row["scenario_id"]: row for row in MATRIX["scenarios"]}
        in_band = [row for row in rows.values() if row.get("peak_in_target_band")]
        self.assertGreaterEqual(len(in_band), 2)
        for row in in_band:
            self.assertGreater(row["target_peak_frequency_cycles_per_sample"], band_low)
            self.assertLess(row["target_peak_frequency_cycles_per_sample"], band_high)
            self.assertTrue(row["scenario_id"] in SCENARIOS)

    def test_seed_identity_is_stable_and_scenario_id_based(self):
        self.assertEqual(stable_scenario_key("example"), stable_scenario_key("example"))
        self.assertNotEqual(stable_scenario_key("example"), stable_scenario_key("other"))
        a_dgp, a_null = replicate_rngs(20261021, "example", 17)
        b_dgp, b_null = replicate_rngs(20261021, "example", 17)
        np.testing.assert_array_equal(a_dgp.standard_normal(16), b_dgp.standard_normal(16))
        np.testing.assert_array_equal(a_null.standard_normal(16), b_null.standard_normal(16))

    def test_shards_cover_replicates_without_overlap(self):
        left = shard_indices(0, 5, 10)
        right = shard_indices(5, 10, 10)
        self.assertEqual(set(left).intersection(right), set())
        self.assertEqual(sorted(left + right), list(range(10)))

    def test_invalid_shard_ranges_are_rejected(self):
        for args in [(-1, 2, 10), (0, 11, 10), (4, 4, 10), (0, 1, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                shard_indices(*args)

    def test_shard_merge_requires_matching_identity_and_no_overlap(self):
        common = {
            "protocol": "pilot", "scenario": "s", "phi": [0.4], "n": 3328,
            "dgp_burn_in": 2000, "surrogates": 200, "total_repetitions": 2,
            "master_seed": 20261021, "scenario_key": 123,
            "matrix_sha256": "matrix", "script_sha256": "script", "commit_sha": "commit"
        }
        left = {
            "run_identity": {**common, "start_index": 0, "stop_index": 1},
            "attempt_records": [{"replicate_index": 0, "status": "VALID"}]
        }
        right = {
            "run_identity": {**common, "start_index": 1, "stop_index": 2},
            "attempt_records": [{"replicate_index": 1, "status": "INVALID"}]
        }
        merged = merge_payloads([left, right], 2)
        self.assertEqual(merged["status"], "PILOT_COMPLETE_DIAGNOSTIC_ONLY")
        self.assertEqual(merged["invalid_attempts"], 1)
        self.assertFalse(merged["formal_calibration_pass"])
        with self.assertRaises(ValueError):
            merge_payloads([left, left], 2)

    def test_shard_merge_rejects_mismatched_commit_identity(self):
        base = {"protocol": "pilot", "scenario": "s", "phi": [0.4], "n": 3328,
                "dgp_burn_in": 2000, "surrogates": 200, "total_repetitions": 2,
                "master_seed": 20261021, "scenario_key": 123,
                "matrix_sha256": "matrix", "script_sha256": "script", "commit_sha": "commit"}
        a = {"run_identity": {**base, "start_index": 0, "stop_index": 1}, "attempt_records": []}
        bbase = dict(base, commit_sha="other")
        b = {"run_identity": {**bbase, "start_index": 1, "stop_index": 2}, "attempt_records": []}
        with self.assertRaises(ValueError):
            merge_payloads([a, b], 2)


if __name__ == "__main__":
    unittest.main()
