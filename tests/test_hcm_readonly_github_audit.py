"""Static regression tests for the HCM read-only GitHub audit script."""
from pathlib import Path
import re
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "hcm_readonly_github_audit.sh"
SOURCE = SCRIPT.read_text(encoding="utf-8")


def gh_api_commands(source: str) -> list[str]:
    """Return complete multiline gh api command strings for static review."""
    lines = source.splitlines()
    commands: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if re.search(r"\bgh\s+api\b", line) and not line.lstrip().startswith("#"):
            parts = [line]
            while parts[-1].rstrip().endswith("\\") and index + 1 < len(lines):
                index += 1
                parts.append(lines[index])
            commands.append(" ".join(part.rstrip().rstrip("\\") for part in parts))
        index += 1
    return commands


class ReadOnlyAuditScriptTests(unittest.TestCase):
    def test_review_branch_name_is_encoded_in_both_api_paths(self):
        self.assertGreaterEqual(SOURCE.count("branches/review%2Ftype1-v4-remediation"), 2)
        self.assertNotRegex(SOURCE, r"branches/review/type1-v4-remediation")

    def test_both_branch_heads_are_captured(self):
        self.assertIn('"main_branch"', SOURCE)
        self.assertIn('"review_branch"', SOURCE)

    def test_both_branch_protection_endpoints_are_captured(self):
        self.assertIn('"main_branch_protection"', SOURCE)
        self.assertIn('"review_branch_protection"', SOURCE)

    def test_orphan_and_known_workflow_ids_are_queried_read_only(self):
        self.assertIn("actions/workflows/398736460", SOURCE)
        self.assertIn("actions/workflows/380113480", SOURCE)
        self.assertIn('"orphan_workflow_398736460"', SOURCE)
        self.assertIn('"acquire_secondary_workflow_380113480"', SOURCE)

    def test_run_history_is_captured_for_all_main_and_review(self):
        self.assertIn('"repos/$REPO/actions/runs?per_page=100"', SOURCE)
        self.assertIn('"repos/$REPO/actions/runs?branch=main&per_page=100"', SOURCE)
        self.assertIn('"repos/$REPO/actions/runs?branch=review%2Ftype1-v4-remediation&per_page=100"', SOURCE)
        self.assertIn("workflow_id,path,head_branch,head_sha,event,status,conclusion", SOURCE)

    def test_every_github_api_command_is_explicit_get(self):
        commands = gh_api_commands(SOURCE)
        self.assertEqual(len(commands), 2)
        for command in commands:
            self.assertIn("--method GET", command)

    def test_no_mutating_or_dispatch_operation_is_present(self):
        self.assertNotRegex(SOURCE, r"--method\s+(POST|PUT|PATCH|DELETE)\b")
        self.assertNotRegex(SOURCE, r"gh\s+workflow\s+(run|enable|disable)\b")
        self.assertNotIn("/dispatches", SOURCE)
        self.assertNotRegex(SOURCE, r"gh\s+pr\s+merge\b")
        self.assertNotRegex(SOURCE, r"\bgit\s+push\b")

    def test_authentication_status_is_checked_without_printing_a_token(self):
        self.assertIn("gh auth status >/dev/null", SOURCE)
        self.assertNotIn("gh auth token", SOURCE)
        self.assertNotRegex(SOURCE, r"(GITHUB_TOKEN|GH_TOKEN)\s*[:=]")

    def test_timestamped_metadata_and_hash_manifest_are_written(self):
        self.assertIn('observed_at_utc=$OBSERVED_AT_UTC', SOURCE)
        self.assertIn('read_only=true', SOURCE)
        self.assertIn('workflow_dispatch_performed=false', SOURCE)
        self.assertIn('! -name SHA256SUMS', SOURCE)
        self.assertIn('sha256sum >"$OUT/SHA256SUMS"', SOURCE)

    def test_strict_shell_mode_is_enabled(self):
        self.assertIn("set -Eeuo pipefail", SOURCE)


if __name__ == "__main__":
    unittest.main()
