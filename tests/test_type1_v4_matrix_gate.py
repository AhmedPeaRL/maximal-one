from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from analysis import calibrate_null_type1
from analysis import calibrate_null_type1_scenario


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_MATRIX = (
    "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
)


class Type1V4MatrixGateTests(unittest.TestCase):
    def test_runner_points_to_v4_candidate_not_v3(self):
        self.assertEqual(
            calibrate_null_type1.MATRIX_PATH.as_posix(),
            EXPECTED_MATRIX,
        )
        self.assertNotIn(
            "TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json",
            calibrate_null_type1.MATRIX_PATH.as_posix(),
        )

    def test_candidate_matrix_is_not_mistaken_for_approval(self):
        matrix_path = ROOT / EXPECTED_MATRIX
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))

        self.assertEqual(
            matrix.get("protocol"),
            "HCM_TYPE1_CALIBRATION_V4_CANDIDATE",
        )

        # Until the formal review and authorization are complete,
        # the candidate must not open the execution gate.
        self.assertFalse(calibrate_null_type1.V4_APPROVED)
        self.assertNotEqual(matrix.get("status"), "APPROVED_FROZEN")
        self.assertNotEqual(matrix.get("freeze_state"), "FROZEN")
        self.assertIsNot(
            matrix.get("confirmatory_execution_authorized"),
            True,
        )

    def test_scenario_runner_blocks_before_argument_parsing(self):
        with patch("sys.argv", ["calibrate_null_type1_scenario"]):
            with self.assertRaisesRegex(
                SystemExit,
                "BLOCKED: V4 matrix is not approved",
            ):
                calibrate_null_type1_scenario.main()


if __name__ == "__main__":
    unittest.main()
