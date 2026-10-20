from __future__ import annotations

import unittest

import numpy as np
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import analysis.type1_calibration_pilot as pilot
from analysis.type1_calibration_pilot import (
    execute_attempt,
    atomic_write,
    load_verified_checkpoint,
)
from analysis.merge_type1_calibration_pilot_shards import merge_payloads
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

    def test_indices_0_to_5_match_connected_shards_reverse_merge_and_resume(self):
        scenario = next(iter(SCENARIOS.values()))
        master_seed = 20261021
        total = 6
        fixture_n = 256
        fixture_burn_in = 32
        fixture_surrogates = 3

        # Deterministic substitutes isolate orchestration and checkpoint behavior.
        # This is NOT a production-equivalence or scientific-validity test.
        def fake_null(series, observed_alpha, rng, trials):
            return {
                "valid": True,
                "trials_requested": trials,
                "null_samples": trials,
                "exceedances": int(abs(observed_alpha) * 10) % (trials + 1),
                "p_value_mc_add_one": 0.25,
                "selected_order": 2,
                "order_selection_diagnostic": {
                    "scientific_role": "test_fixture_only"
                },
            }

        def run_index(index):
            return execute_attempt(
                index=index,
                scenario=scenario,
                master_seed=master_seed,
                surrogates=fixture_surrogates,
                n=fixture_n,
                burn_in=fixture_burn_in,
            )

        with (
            patch(
                "analysis.type1_calibration_pilot.estimate_alpha",
                side_effect=lambda series: float(np.mean(series ** 2)),
            ),
            patch(
                "analysis.type1_calibration_pilot.parametric_short_memory_null",
                side_effect=fake_null,
            ),
        ):
            connected = {i: run_index(i) for i in range(total)}

            shard_ranges = [(0, 2), (2, 4), (4, 6)]
            shard_payloads = []

            for start, stop in shard_ranges:
                identity = {
                    "protocol": "engineering-fixture",
                    "scenario": scenario["scenario_id"],
                    "master_seed": master_seed,
                    "start_index": start,
                    "stop_index": stop,
                }
                shard_payloads.append({
                    "run_identity": identity,
                    "attempt_records": [
                        run_index(i) for i in range(start, stop)
                    ],
                })

            merged = merge_payloads(
                list(reversed(shard_payloads)),
                total_repetitions=total,
            )

            merged_by_index = {
                row["replicate_index"]: row
                for row in merged["attempt_records"]
            }

            self.assertEqual(
                sorted(merged_by_index),
                list(range(6)),
            )

            # Compare all per-index fields, not timing metadata.
            for index in range(total):
                self.assertEqual(
                    connected[index],
                    merged_by_index[index],
                    msg=f"Connected/sharded mismatch at index {index}",
                )

            # Simulate interruption after indices 0 and 1.
            resume_identity = {
                "protocol": "engineering-fixture",
                "scenario": scenario["scenario_id"],
                "master_seed": master_seed,
                "start_index": 0,
                "stop_index": total,
            }

            with tempfile.TemporaryDirectory() as directory:
                checkpoint = Path(directory) / "checkpoint.json"
                atomic_write(checkpoint, {
                    "run_identity": resume_identity,
                    "attempt_records": [
                        connected[0],
                        connected[1],
                    ],
                })

                restored = load_verified_checkpoint(
                    checkpoint,
                    resume_identity,
                )

                resumed = {
                    row["replicate_index"]: row
                    for row in restored["attempt_records"]
                }

                for index in range(2, total):
                    resumed[index] = run_index(index)

                self.assertEqual(
                    sorted(resumed),
                    list(range(6)),
                )

                for index in range(total):
                    self.assertEqual(
                        connected[index],
                        resumed[index],
                        msg=f"Connected/resumed mismatch at index {index}",
                    )

                # The manifest must reject modified artifact bytes.
                checkpoint.write_text(
                    checkpoint.read_text(encoding="utf-8") + " ",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    load_verified_checkpoint(
                        checkpoint,
                        resume_identity,
                    )


if __name__ == "__main__":
    unittest.main()
