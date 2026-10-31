from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (
    ROOT / ".github/workflows/null-type1-calibration.yml"
)


class V3V4GovernanceSeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_v3_authorization_guards_precede_matrix_output(self):
        required = [
            "APPROVED_FROZEN",
            'd.get("freeze_state") != "FROZEN"',
            'd.get("confirmatory_execution_authorized") is not True',
            'd.get("archive_git_identity_verified") is not True',
            'os.environ["GITHUB_OUTPUT"]',
        ]

        positions = [self.text.index(item) for item in required]
        self.assertEqual(positions, sorted(positions))

    def test_v3_calibration_job_fails_closed_before_artifact_binding(self):
        guard = "Fail closed until the V3 runner is reconciled"
        artifact = "Bind artifact to exact workflow identity"

        self.assertIn(guard, self.text)
        self.assertIn(artifact, self.text)
        self.assertLess(
            self.text.index(guard),
            self.text.index(artifact),
        )

        guard_section = self.text[
            self.text.index(guard):
            self.text.index(artifact)
        ]
        self.assertIn("exit 1", guard_section)
        self.assertIn("No calibration is authorized", guard_section)

    def test_v3_workflow_contains_no_executable_v4_runner_command(self):
        forbidden_commands = [
            "python -m analysis.calibrate_null_type1_scenario",
            "python -m analysis.calibrate_null_type1",
            "python analysis/calibrate_null_type1_scenario.py",
            "python analysis/calibrate_null_type1.py",
        ]

        for command in forbidden_commands:
            with self.subTest(command=command):
                self.assertNotIn(command, self.text)

    def test_v3_workflow_does_not_authorize_itself(self):
        self.assertIn(
            'd.get("confirmatory_execution_authorized") is not True',
            self.text,
        )
        self.assertIn(
            "d.get('status') != 'APPROVED_FROZEN'",
            self.text,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
