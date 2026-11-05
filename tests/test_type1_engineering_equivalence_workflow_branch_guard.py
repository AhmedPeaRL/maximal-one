from pathlib import Path
import os
import sys
import unittest
from unittest.mock import patch

from analysis import calibrate_null_type1_scenario as runner

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/type1-v4-engineering-equivalence.yml"
AUTHORIZED = "refs/heads/review/type1-v4-remediation"


class EngineeringEquivalenceBranchGuardTests(unittest.TestCase):
    def test_direct_entrypoint_rejects_non_actions_context_even_on_review_ref(self):
        with patch.dict(os.environ, {"GITHUB_REF": AUTHORIZED}, clear=True):
            with patch.object(sys, "argv", ["calibrate_null_type1_scenario", "--engineering-test"]):
                with self.assertRaisesRegex(SystemExit, "requires GitHub Actions context"):
                    runner.engineering_main()

    def test_workflow_dispatch_has_job_level_branch_and_commit_guard(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn('test "$GITHUB_REF" = "refs/heads/review/type1-v4-remediation"', workflow)
        self.assertIn('test "$(git rev-parse HEAD)" = "$GITHUB_SHA"', workflow)
        self.assertLess(
            workflow.index("Require review branch before engineering execution"),
            workflow.index("Set up Python"),
        )
        self.assertLess(
            workflow.index("Require review branch before engineering execution"),
            workflow.index("Test official-runner connected/sharded/merged/resumed equivalence"),
        )

    def test_direct_engineering_entrypoint_rejects_main_before_output(self):
        with patch.dict(os.environ, {"GITHUB_REF": "refs/heads/main"}, clear=False):
            with patch.object(sys, "argv", ["calibrate_null_type1_scenario", "--engineering-test"]):
                with self.assertRaisesRegex(SystemExit, "BLOCKED:"):
                    runner.engineering_main()

    def test_direct_engineering_entrypoint_rejects_missing_branch(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(sys, "argv", ["calibrate_null_type1_scenario", "--engineering-test"]):
                with self.assertRaisesRegex(SystemExit, "BLOCKED:"):
                    runner.engineering_main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
