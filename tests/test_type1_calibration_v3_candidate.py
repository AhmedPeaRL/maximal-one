from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess

from analysis.calibrate_null_type1 import (
    MATRIX, SCENARIO_ORDER, SCENARIOS, acceptance_decision,
    replicate_rngs, wilson_upper_one_sided,
)


class TypeICalibrationV3CandidateTests(unittest.TestCase):
    def test_freeze_state_and_authorization_are_consistent(self):
        if MATRIX["status"] == "CANDIDATE_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW":
            self.assertEqual(MATRIX["freeze_state"], "NOT_FROZEN")
            self.assertFalse(MATRIX["confirmatory_execution_authorized"])
        elif MATRIX["status"] == "APPROVED_FROZEN":
            self.assertEqual(MATRIX["freeze_state"], "FROZEN")
            self.assertTrue(MATRIX["confirmatory_execution_authorized"])
        else:
            self.fail(f"Unexpected protocol status: {MATRIX['status']}")
        self.assertFalse(MATRIX["claim_support"])
        self.assertFalse(MATRIX["promotion_authority"])

    def test_matrix_and_design_dimensions_are_exact(self):
        p = MATRIX["primary_design"]
        self.assertEqual(len(SCENARIO_ORDER), 9)
        self.assertEqual(len(set(SCENARIO_ORDER)), 9)
        self.assertEqual(p["outer_repetitions_per_scenario"], 2000)
        self.assertEqual(p["surrogates_requested_per_outer_replicate"], 1000)
        self.assertEqual(p["sample_size"], 1024)
        self.assertEqual(p["nominal_alpha"], 0.05)
        self.assertEqual(p["one_sided_upper_bound_maximum"], 0.075)

    def test_every_declared_dgp_is_stationary(self):
        for scenario, phi in SCENARIOS.items():
            with self.subTest(scenario=scenario):
                ar = np.asarray([1.0] + [-float(v) for v in phi])
                self.assertTrue(bool(ArmaProcess(ar=ar, ma=np.asarray([1.0])).isstationary))

    def test_seed_is_reproducible_and_shard_order_invariant(self):
        # Ask for replicates in reverse order, then compare the same identities.
        first = {}
        for idx in [0, 1, 7, 23, 100]:
            dgp, null = replicate_rngs(20261019, 2, idx)
            first[idx] = (dgp.standard_normal(8), null.standard_normal(8))
        second = {}
        for idx in [100, 23, 7, 1, 0]:
            dgp, null = replicate_rngs(20261019, 2, idx)
            second[idx] = (dgp.standard_normal(8), null.standard_normal(8))
        for idx in first:
            np.testing.assert_array_equal(first[idx][0], second[idx][0])
            np.testing.assert_array_equal(first[idx][1], second[idx][1])

    def test_one_sided_upper_bound_is_used_not_two_sided_containment(self):
        # 49/1000: the one-sided upper bound should be below the 0.075 ceiling.
        upper = wilson_upper_one_sided(49, 1000)
        self.assertLess(upper, 0.075)
        # A two-sided interval is intentionally not an input to the acceptance rule.
        passed, status = acceptance_decision(requested=2000, completed=2000, invalid=0, upper=upper)
        self.assertTrue(passed)
        self.assertEqual(status, "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE")

    def test_any_invalid_attempt_blocks_pass(self):
        passed, status = acceptance_decision(requested=2000, completed=2000, invalid=1, upper=0.04)
        self.assertFalse(passed)
        self.assertEqual(status, "TYPE1_CALIBRATION_FAILED_INVALID_ATTEMPTS")

    def test_incomplete_run_never_passes(self):
        passed, status = acceptance_decision(requested=2000, completed=1999, invalid=0, upper=0.04)
        self.assertFalse(passed)
        self.assertEqual(status, "INCOMPLETE_NOT_A_PASS")

    def test_calibration_parameters_match_declared_production_configuration(self):
        strict = json.loads(Path("core-scientific/strict_claim.json").read_text(encoding="utf-8"))
        null_protocol = strict["stochastic_null_protocol"]
        self.assertEqual(null_protocol["bootstrap_trials"], MATRIX["primary_design"]["surrogates_requested_per_outer_replicate"])
        self.assertEqual(null_protocol["burn_in"], MATRIX["production_equivalence_requirements"]["surrogate_generation_burn_in"])
        self.assertEqual(null_protocol["order_selection"]["min_order"], 1)
        self.assertEqual(null_protocol["order_selection"]["max_order"], 20)
        self.assertEqual(null_protocol["order_selection"]["criterion"], "AIC")
        self.assertEqual(null_protocol["order_selection"]["trend"], "constant")
        self.assertEqual(null_protocol["p_value_rule"], "(exceedances + 1) / (valid_surrogates + 1)")
        from analysis.numerical_spectral_verification import DEFAULT_FREQ_MIN, DEFAULT_FREQ_MAX, CANONICAL_NPERSEG
        from analysis.appropriate_stochastic_null import MAX_AR_ORDER, MIN_AR_ORDER, MIN_VALID_SURROGATES, COMPARISON_HOLD_BACK
        self.assertEqual((DEFAULT_FREQ_MIN, DEFAULT_FREQ_MAX), (0.01, 0.05))
        self.assertEqual(CANONICAL_NPERSEG, 1024)
        self.assertEqual((MIN_AR_ORDER, MAX_AR_ORDER), (1, 20))
        self.assertEqual(COMPARISON_HOLD_BACK, 20)
        self.assertEqual(MIN_VALID_SURROGATES, 200)
        self.assertEqual(MATRIX["primary_design"]["surrogates_requested_per_outer_replicate"], 1000)

    def test_scenario_matrix_is_the_single_source_for_workflow_scenarios(self):
        workflow = Path('.github/workflows/null-type1-calibration.yml').read_text(encoding='utf-8')
        self.assertIn('TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json', workflow)
        self.assertIn("d.get('status') != 'APPROVED_FROZEN'", workflow)
        self.assertIn('outer_repetitions_per_scenario', Path('protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
