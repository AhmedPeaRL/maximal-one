from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from analysis import calibrate_null_type1 as runner
from analysis import calibrate_null_type1_scenario as scenario_runner


ROOT = Path(__file__).resolve().parents[1]
MATRIX_RELATIVE_PATH = (
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
)
MATRIX_PATH = ROOT / MATRIX_RELATIVE_PATH


class Type1V4MatrixGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = json.loads(
            MATRIX_PATH.read_text(encoding="utf-8")
        )
        cls.design = cls.matrix["candidate_dimensions_not_frozen"]

    def test_runner_uses_exact_v4_candidate_path(self):
        self.assertEqual(
            runner.MATRIX_PATH.resolve(),
            MATRIX_PATH.resolve(),
        )

    def test_candidate_matrix_is_not_authorization(self):
        self.assertEqual(
            self.matrix["protocol"],
            "HCM_TYPE1_CALIBRATION_V4_CANDIDATE",
        )
        self.assertEqual(self.matrix["freeze_state"], "NOT_FROZEN")
        self.assertIs(
            self.matrix["confirmatory_execution_authorized"], False
        )
        self.assertIs(self.matrix["claim_support"], False)
        self.assertIs(self.matrix["promotion_authority"], False)
        self.assertFalse(runner.V4_APPROVED)

    def test_runtime_dimensions_match_candidate_without_defaults(self):
        self.assertEqual(
            runner.REQUIRED_SAMPLE_SIZE,
            self.design["sample_size"],
        )
        self.assertEqual(
            runner.DGP_BURN_IN,
            self.design["dgp_burn_in"],
        )
        self.assertEqual(
            runner.REQUIRED_OUTER_REPETITIONS,
            self.design["outer_repetitions_per_scenario"],
        )
        self.assertEqual(
            runner.REQUIRED_SURROGATES,
            self.design["surrogates_requested_per_outer_replicate"],
        )
        self.assertEqual(
            runner.NOMINAL_ALPHA,
            self.design["nominal_alpha"],
        )
        self.assertEqual(
            runner.MASTER_SEED,
            self.design["master_seed_candidate"],
        )

    def test_all_nine_scenarios_match_matrix_identity_and_coefficients(self):
        expected = {
            row["scenario_id"]: row["phi"]
            for row in self.matrix["scenarios"]
        }
        self.assertEqual(len(expected), 9)
        self.assertEqual(len(set(expected)), 9)
        self.assertEqual(runner.SCENARIOS, expected)
        self.assertEqual(runner.SCENARIO_ORDER, list(expected))

    def test_seed_identity_uses_scenario_id_not_list_position(self):
        scenario_a = self.matrix["scenarios"][0]["scenario_id"]
        scenario_b = self.matrix["scenarios"][1]["scenario_id"]

        key_a = runner.stable_scenario_key(scenario_a)
        key_b = runner.stable_scenario_key(scenario_b)

        self.assertIsInstance(key_a, int)
        self.assertIsInstance(key_b, int)
        self.assertNotEqual(key_a, key_b)

        seq_a = runner.seed_sequence(20261021, scenario_a, 0, 0)
        seq_b = runner.seed_sequence(20261021, scenario_b, 0, 0)

        self.assertNotEqual(
            seq_a.generate_state(4).tolist(),
            seq_b.generate_state(4).tolist(),
        )

    def test_acceptance_rule_remains_unresolved_and_cannot_pass(self):
        self.assertIsNone(self.design["acceptance_rule"])
        self.assertIsNone(runner.ACCEPTANCE_RULE)
        self.assertIsNone(runner.MAX_ACCEPTABLE_WILSON_UPPER)

        passed, reason = runner.acceptance_decision(
            requested=2000,
            completed=2000,
            invalid=0,
            upper=0.01,
        )
        self.assertFalse(passed)
        self.assertEqual(reason, "BLOCKED_ACCEPTANCE_RULE_UNRESOLVED")

    def test_scenario_runner_blocks_before_parsing_or_simulation(self):
        with patch("sys.argv", ["calibrate_null_type1_scenario"]):
            with self.assertRaisesRegex(
                SystemExit,
                "BLOCKED: V4 matrix is not approved",
            ):
                scenario_runner.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
