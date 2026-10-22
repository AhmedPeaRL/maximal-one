from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from analysis import calibrate_null_type1
from analysis import calibrate_null_type1_scenario


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

    def test_runner_references_the_intended_v4_candidate(self):
        self.assertEqual(
            calibrate_null_type1.MATRIX_PATH.as_posix(),
            MATRIX_RELATIVE_PATH,
        )

    def test_candidate_status_never_authorizes_formal_execution(self):
        self.assertEqual(
            self.matrix["protocol"],
            "HCM_TYPE1_CALIBRATION_V4_CANDIDATE",
        )
        self.assertEqual(
            self.matrix["freeze_state"],
            "NOT_FROZEN",
        )
        self.assertIs(
            self.matrix["confirmatory_execution_authorized"],
            False,
        )
        self.assertIs(
            self.matrix["claim_support"],
            False,
        )
        self.assertIs(
            self.matrix["promotion_authority"],
            False,
        )
        self.assertFalse(calibrate_null_type1.V4_APPROVED)

    def test_runner_maps_every_candidate_dimension_without_defaults(self):
        # These assertions must pass only after the implementation has
        # explicitly mapped the V4 schema to its runtime configuration.
        self.assertEqual(
            calibrate_null_type1.REQUIRED_SAMPLE_SIZE,
            self.design["sample_size"],
        )
        self.assertEqual(
            calibrate_null_type1.REQUIRED_OUTER_REPETITIONS,
            self.design["outer_repetitions_per_scenario"],
        )
        self.assertEqual(
            calibrate_null_type1.REQUIRED_SURROGATES,
            self.design["surrogates_requested_per_outer_replicate"],
        )
        self.assertEqual(
            calibrate_null_type1.NOMINAL_ALPHA,
            self.design["nominal_alpha"],
        )
        self.assertEqual(
            calibrate_null_type1.MASTER_SEED,
            self.design["master_seed_candidate"],
        )

    def test_runner_loads_all_nine_scenarios_from_the_matrix(self):
        expected = {
            row["scenario_id"]: row["phi"]
            for row in json.loads(
                MATRIX_PATH.read_text(encoding="utf-8")
            )["scenarios"]
        }
        self.assertEqual(len(expected), 9)
        self.assertEqual(
            calibrate_null_type1.SCENARIOS,
            expected,
        )

    def test_unresolved_acceptance_rule_cannot_become_a_threshold(self):
        self.assertIsNone(self.design["acceptance_rule"])
        self.assertFalse(calibrate_null_type1.V4_APPROVED)

    def test_scenario_runner_blocks_before_argument_parsing(self):
        with patch(
            "sys.argv",
            ["calibrate_null_type1_scenario"],
        ):
            with self.assertRaisesRegex(
                SystemExit,
                "BLOCKED: V4 matrix is not approved",
            ):
                calibrate_null_type1_scenario.main()


if __name__ == "__main__":
    unittest.main()
