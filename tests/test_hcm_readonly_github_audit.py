"""Static regression tests for the HCM read-only GitHub audit script."""
from pathlib import Path
import re
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "hcm_readonly_github_audit.sh"
SOURCE = SCRIPT.read_text(encoding="utf-8")


class ReadOnlyAuditScriptTests(unittest.TestCase):
    def test_review_branch_name_is_url_encoded_in_api_paths(self):
        self.assertIn("branches/review%2Ftype1-v4-remediation", SOURCE)
        self.assertNotRegex(SOURCE, r"branches/review/type1-v4-remediation")

    def test_both_branch_protection_endpoints_are_captured(self):
        self.assertIn('"main_branch_protection"', SOURCE)
        self.assertIn('"review_branch_protection"', SOURCE)

    def test_all_github_api_calls_are_explicit_get_requests(self):
        calls = re.findall(r"gh\s+api([^\n]*)", SOURCE)
        self.assertGreaterEqual(len(calls), 2)
        for call in calls:
            self.assertIn("--method GET", call)
        self.assertNotRegex(SOURCE, r"--method\s+(POST|PUT|PATCH|DELETE)\b")

    def test_script_does_not_dispatch_or_enable_workflows(self):
        self.assertNotRegex(SOURCE, r"gh\s+workflow\s+(run|enable|disable)\b")
        self.assertNotIn("/actions/workflows/", SOURCE)


if __name__ == "__main__":
    unittest.main()
