from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from analysis import type1_calibration_pilot as pilot


ROOT = Path(__file__).resolve().parents[1]
GUARD_SCRIPT = ROOT / "scripts" / "type1_runtime_pilot_branch_guard.py"
WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "type1-calibration-runtime-pilot.yml"
)


class RuntimePilotBranchGuardTests(unittest.TestCase):

    def test_unauthorized_main_branch_is_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "artifacts"

            env = os.environ.copy()
            env["GITHUB_REF"] = "refs/heads/main"

            result = subprocess.run(
                [sys.executable, str(GUARD_SCRIPT)],
                cwd=directory,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BLOCKED:", result.stderr)
            self.assertIn("refs/heads/main", result.stderr)
            self.assertFalse(output_dir.exists())

    def test_authorized_review_branch_passes_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            env = os.environ.copy()
            env["GITHUB_REF"] = (
                "refs/heads/review/type1-v4-remediation"
            )

            result = subprocess.run(
                [sys.executable, str(GUARD_SCRIPT)],
                cwd=directory,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Authorized runtime-pilot branch", result.stdout)

    def test_runner_entry_point_rejects_unauthorized_branch_first(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "artifacts" / "pilot.json"

            with patch.dict(
                os.environ,
                {"GITHUB_REF": "refs/heads/main"},
            ):
                with patch.object(sys, "argv", ["type1_calibration_pilot"]):
                    with self.assertRaisesRegex(SystemExit, "BLOCKED:"):
                        pilot.main()

            self.assertFalse(output.exists())
            self.assertFalse(output.parent.exists())

    def test_workflow_guard_precedes_output_creation_and_runner(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        guard_position = workflow.index(
            "python scripts/type1_runtime_pilot_branch_guard.py"
        )
        output_position = workflow.index("mkdir -p artifacts")
        runner_position = workflow.index(
            "python -m analysis.type1_calibration_pilot"
        )

        self.assertLess(guard_position, output_position)
        self.assertLess(guard_position, runner_position)


if __name__ == "__main__":
    unittest.main()
