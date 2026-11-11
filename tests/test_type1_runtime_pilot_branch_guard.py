from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from analysis import type1_calibration_pilot as pilot
from scripts import type1_runtime_pilot_branch_guard as guard


ROOT = Path(__file__).resolve().parents[1]
GUARD_SCRIPT = ROOT / "scripts" / "type1_runtime_pilot_branch_guard.py"
WORKFLOW = ROOT / ".github" / "workflows" / "type1-calibration-runtime-pilot.yml"

AUTHORIZED = "refs/heads/review/type1-v4-remediation"


def current_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()


class RuntimePilotBranchGuardTests(unittest.TestCase):

    def test_unauthorized_main_branch_is_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "artifacts"
            env = os.environ.copy()
            env.update({
                "GITHUB_ACTIONS": "true",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_SHA": current_sha(),
            })

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

    def test_spoofed_authorized_ref_without_actions_is_rejected(self):
        env = os.environ.copy()
        env.pop("GITHUB_ACTIONS", None)
        env["GITHUB_REF"] = AUTHORIZED
        env["GITHUB_SHA"] = current_sha()

        result = subprocess.run(
            [sys.executable, str(GUARD_SCRIPT)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires GitHub Actions context", result.stderr)

    def test_missing_github_sha_is_rejected(self):
        env = os.environ.copy()
        env.update({
            "GITHUB_ACTIONS": "true",
            "GITHUB_REF": AUTHORIZED,
        })
        env.pop("GITHUB_SHA", None)

        result = subprocess.run(
            [sys.executable, str(GUARD_SCRIPT)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("full 40-character GITHUB_SHA", result.stderr)

    def test_authorized_review_branch_passes_guard(self):
        env = os.environ.copy()
        env.update({
            "GITHUB_ACTIONS": "true",
            "GITHUB_REF": AUTHORIZED,
            "GITHUB_SHA": current_sha(),
        })

        result = subprocess.run(
            [sys.executable, str(GUARD_SCRIPT)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Authorized runtime-pilot branch", result.stdout)

    def test_runner_entry_point_rejects_unauthorized_branch_first(self):
        output = ROOT / "artifacts" / "pilot-should-not-exist.json"

        with patch.dict(
            os.environ,
            {
                "GITHUB_ACTIONS": "true",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_SHA": current_sha(),
            },
            clear=True,
        ):
            with patch.object(sys, "argv", ["type1_calibration_pilot"]):
                with self.assertRaisesRegex(SystemExit, "BLOCKED:"):
                    pilot.main()

        self.assertFalse(output.exists())

    def test_runner_entry_point_rejects_spoofed_ref_without_actions(self):
        with patch.dict(
            os.environ,
            {
                "GITHUB_REF": AUTHORIZED,
                "GITHUB_SHA": current_sha(),
            },
            clear=True,
        ):
            with patch.object(sys, "argv", ["type1_calibration_pilot"]):
                with self.assertRaisesRegex(
                    SystemExit,
                    "requires GitHub Actions context",
                ):
                    pilot.main()

    def test_runner_entry_point_rejects_checkout_sha_mismatch(self):
        with patch.dict(
            os.environ,
            {
                "GITHUB_ACTIONS": "true",
                "GITHUB_REF": AUTHORIZED,
                "GITHUB_SHA": "a" * 40,
            },
            clear=True,
        ):
            with patch.object(
                guard.subprocess,
                "check_output",
                return_value="b" * 40,
            ):
                with patch.object(sys, "argv", ["type1_calibration_pilot"]):
                    with self.assertRaisesRegex(
                        SystemExit,
                        "checkout differs from GITHUB_SHA",
                    ):
                        pilot.main()

    def test_workflow_guards_precede_output_creation_and_runner(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        guard_position = workflow.index(
            "python scripts/type1_runtime_pilot_branch_guard.py"
        )
        checkout_position = workflow.index(
            'actual_head="$(git rev-parse HEAD)"'
        )
        output_position = workflow.index("mkdir -p artifacts")
        runner_position = workflow.index(
            "python -m analysis.type1_calibration_pilot"
        )

        self.assertLess(guard_position, checkout_position)
        self.assertLess(checkout_position, output_position)
        self.assertLess(output_position, runner_position)


if __name__ == "__main__":
    unittest.main(verbosity=2)
