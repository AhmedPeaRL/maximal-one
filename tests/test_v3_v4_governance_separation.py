import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class V3V4GovernanceSeparationTests(unittest.TestCase):
    def test_legacy_workflow_remains_pinned_to_v3(self):
        workflow = (
            ROOT / ".github/workflows/null-type1-calibration.yml"
        ).read_text(encoding="utf-8")

        runner = (
            ROOT / "analysis/calibrate_null_type1.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json",
            workflow,
        )
        self.assertIn(
            'MATRIX_PATH = Path("protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json")',
            runner,
        )
        self.assertNotIn(
            "TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json",
            workflow,
        )

    def test_v4_candidate_is_not_an_authorization_record(self):
        matrix_path = (
            ROOT
            / "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
        )
        matrix = json.loads(
            matrix_path.read_text(encoding="utf-8")
        )

        self.assertEqual(
            matrix["freeze_state"],
            "NOT_FROZEN",
        )
        self.assertIs(
            matrix["confirmatory_execution_authorized"],
            False,
        )
        self.assertIs(matrix["claim_support"], False)
        self.assertIs(matrix["promotion_authority"], False)
        self.assertIsNone(
            matrix["candidate_dimensions_not_frozen"]["acceptance_rule"]
        )
        self.assertEqual(
            matrix["approval_record"]["approval_status"],
            "NOT_APPROVED",
        )

    def test_engineering_workflow_is_separate(self):
        workflow_path = (
            ROOT
            / ".github/workflows/type1-v4-engineering-equivalence.yml"
        )
        workflow = workflow_path.read_text(encoding="utf-8")

        self.assertIn(
            "Type-I V4 Official Runner Engineering Equivalence",
            workflow,
        )
        self.assertIn(
            "tests.test_type1_cli_resume_identity_rejections",
            workflow,
        )
        self.assertIn(
            "tests.test_type1_full_path_equivalence",
            workflow,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
