from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = (
    ROOT
    / ".github/workflows/type1-v4-cross-runner-worker-order.yml"
)
REQUIRED_REF = (
    'test "$GITHUB_REF" = '
    '"refs/heads/review/type1-v4-remediation"'
)
REQUIRED_HEAD = (
    'test "$(git rev-parse HEAD)" = "$GITHUB_SHA"'
)


def extract_job(workflow: str, job_name: str) -> str:
    marker = f"  {job_name}:\n"
    start = workflow.index(marker) + len(marker)
    next_job = re.search(
        r"(?m)^  [A-Za-z0-9_-]+:\s*$",
        workflow[start:],
    )
    end = start + next_job.start() if next_job else len(workflow)
    return workflow[start:end]


class CrossRunnerWorkflowBranchGuardTests(unittest.TestCase):
    def test_all_jobs_require_review_branch_before_execution(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        jobs = {
            "connected-reference": (
                "python -m analysis.calibrate_null_type1_scenario"
            ),
            "independent-workers": (
                "python -m analysis.calibrate_null_type1_scenario"
            ),
            "compare": (
                "python -m analysis.compare_type1_cross_runner"
            ),
        }

        for job_name, invocation in jobs.items():
            with self.subTest(job=job_name):
                section = extract_job(workflow, job_name)

                self.assertIn(REQUIRED_REF, section)
                self.assertIn(REQUIRED_HEAD, section)

                guard_position = section.index(REQUIRED_REF)
                self.assertLess(
                    guard_position,
                    section.index("- name: Set up Python"),
                )
                self.assertLess(
                    guard_position,
                    section.index(invocation),
                )

    def test_workflow_stays_engineering_only(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("--engineering-test", workflow)
        self.assertNotIn("formal_calibration_pass: true", workflow)


if __name__ == "__main__":
    unittest.main(verbosity=2)
