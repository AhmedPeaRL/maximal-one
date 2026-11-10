from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from analysis import type1_calibration_pilot as pilot

ROOT = Path(__file__).resolve().parents[1]
GUARD_SCRIPT = ROOT / "scripts" / "type1_runtime_pilot_branch_guard.py"
WORKFLOW = ROOT / ".github" / "workflows" / "type1-calibration-runtime-pilot.yml"
AUTHORIZED_REF = "refs/heads/review/type1-v4-remediation"


def current_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def run_guard(updates: dict[str, str], remove: tuple[str, ...] = ()):
    env = os.environ.copy()
    for key in remove:
        env.pop(key, None)
    env.update(updates)
    return subprocess.run(
        [sys.executable, str(GUARD_SCRIPT)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class RuntimePilotBranchGuardTests(unittest.TestCase):
    def test_unauthorized_main_branch_is_rejected(self):
        result = run_guard({"GITHUB_REF": "refs/heads/main"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKED:", result.stderr)
        self.assertIn("refs/heads/main", result.stderr)

    def test_authorized_review_branch_and_exact_checkout_pass(self):
        result = run_guard({
            "GITHUB_REF": AUTHORIZED_REF,
            "GITHUB_ACTIONS": "true",
            "GITHUB_SHA": current_head(),
        })
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Authorized runtime-pilot branch and checkout", result.stdout)

    def test_missing_github_actions_context_is_rejected(self):
        result = run_guard({
            "GITHUB_REF": AUTHORIZED_REF,
            "GITHUB_SHA": current_head(),
        }, remove=("GITHUB_ACTIONS",))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires the GitHub Actions execution context", result.stderr)

    def test_missing_github_sha_is_rejected(self):
        result = run_guard({
            "GITHUB_REF": AUTHORIZED_REF,
            "GITHUB_ACTIONS": "true",
        }, remove=("GITHUB_SHA",))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("full 40-character GITHUB_SHA", result.stderr)

    def test_mismatched_checkout_sha_is_rejected(self):
        result = run_guard({
            "GITHUB_REF": AUTHORIZED_REF,
            "GITHUB_ACTIONS": "true",
            "GITHUB_SHA": "0" * 40,
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checkout does not match GITHUB_SHA", result.stderr)

    def test_runner_entry_point_rejects_unauthorized_branch_before_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "artifacts" / "pilot.json"
            from unittest.mock import patch
            with patch.dict(os.environ, {"GITHUB_REF": "refs/heads/main"}):
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
        runner_position = workflow.index("python -m analysis.type1_calibration_pilot")
        self.assertLess(guard_position, output_position)
        self.assertLess(guard_position, runner_position)


if __name__ == "__main__":
    unittest.main()
