from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
OUTPUT_DIR = ROOT / "artifacts"


class ReviewV4NegativeGateTests(unittest.TestCase):
    def test_unfrozen_v4_matrix_blocks_formal_runner_before_output(self):
        matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        frozen = (
            matrix.get("status") == "APPROVED_FROZEN"
            and matrix.get("freeze_state") == "FROZEN"
            and matrix.get("confirmatory_execution_authorized") is True
        )
        if frozen:
            self.fail(
                "The V4 matrix is now marked frozen/authorized. Do not run this "
                "negative test against an authorized protocol; obtain a new "
                "independent review and a separately designed safe test fixture."
            )

        env = os.environ.copy()
        env.update({
            "GITHUB_ACTIONS": "true",
            "GITHUB_REF": "refs/heads/review/type1-v4-remediation",
            "GITHUB_SHA": subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=ROOT,
                text=True,
            ).strip(),
        })

        scenarios = matrix.get("scenarios")
        self.assertIsInstance(scenarios, list)
        self.assertTrue(scenarios)
        scenario = scenarios[0].get("scenario_id")
        self.assertIsInstance(scenario, str)

        output = OUTPUT_DIR / f"null_type1_calibration_{scenario}.json"
        self.assertFalse(output.exists(), "Pre-existing output makes this test ambiguous.")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "analysis.calibrate_null_type1_scenario",
                "--scenario",
                scenario,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
            env=env,
        )

        self.assertNotEqual(result.returncode, 0)

        combined = result.stdout + "\n" + result.stderr

        self.assertIn("BLOCKED:", combined)
        self.assertIn(
            "matrix has no independently approved_design",
            combined,
        )

        self.assertFalse(
            output.exists(),
            "Blocked runner created a calibration output.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
