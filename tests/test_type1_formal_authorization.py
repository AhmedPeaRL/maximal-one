from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from analysis import calibrate_null_type1_scenario as scenario_runner
from analysis.type1_formal_authorization import require_formal_authorization


ROOT = Path(__file__).resolve().parents[1]


def current_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()


def authorized_test_environment() -> dict[str, str]:
    return {
        "GITHUB_ACTIONS": "true",
        "GITHUB_REF": "refs/heads/review/type1-v4-remediation",
        "GITHUB_SHA": current_head(),
    }


class FormalAuthorizationNegativeTests(unittest.TestCase):

    def test_local_execution_is_blocked(self):
        env = authorized_test_environment()
        env["GITHUB_ACTIONS"] = "false"

        with patch.dict(os.environ, env, clear=False):
            with self.assertRaisesRegex(
                SystemExit,
                "formal calibration requires GitHub Actions context",
            ):
                require_formal_authorization(ROOT)

    def test_wrong_branch_is_blocked(self):
        env = authorized_test_environment()
        env["GITHUB_REF"] = "refs/heads/main"

        with patch.dict(os.environ, env, clear=False):
            with self.assertRaisesRegex(
                SystemExit,
                "formal calibration is restricted",
            ):
                require_formal_authorization(ROOT)

    def test_checkout_sha_mismatch_is_blocked(self):
        env = authorized_test_environment()
        env["GITHUB_SHA"] = "0" * 40

        with patch.dict(os.environ, env, clear=False):
            with self.assertRaisesRegex(
                SystemExit,
                "GITHUB_SHA does not match",
            ):
                require_formal_authorization(ROOT)

    def test_current_candidate_matrix_has_no_approved_design(self):
        env = authorized_test_environment()

        with patch.dict(os.environ, env, clear=False):
            with self.assertRaisesRegex(
                SystemExit,
                "no independently approved_design",
            ):
                require_formal_authorization(ROOT)

    def test_formal_runner_blocks_before_any_attempt_or_output(self):
        env = authorized_test_environment()
        scenario = scenario_runner.SCENARIO_ORDER[0]

        output = (
            ROOT
            / "artifacts"
            / f"null_type1_calibration_{scenario}.json"
        )

        if output.exists():
            self.fail(
                "Pre-existing formal output makes this negative test ambiguous."
            )

        with (
            patch.dict(os.environ, env, clear=False),
            patch(
                "sys.argv",
                ["calibrate_null_type1_scenario", "--scenario", scenario],
            ),
            patch.object(
                scenario_runner,
                "execute_attempt",
                side_effect=AssertionError(
                    "Formal simulation must not reach execute_attempt."
                ),
            ),
        ):
            with self.assertRaisesRegex(
                SystemExit,
                "no independently approved_design",
            ):
                scenario_runner.main()

        self.assertFalse(
            output.exists(),
            "Blocked formal runner created an output file.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
