import unittest
from unittest.mock import patch

from scripts.audit_type1_governance_refs import (
    EXCLUDED_GENERATED_PATHS,
    _line_matches,
    classify,
    inspect_ref,
)


class OccurrenceLocalInventoryTests(unittest.TestCase):
    def test_runner_invocation_line_is_candidate(self):
        result, _ = classify(
            ".github/workflows/example.yml",
            "python -m analysis.calibrate_null_type1_scenario --scenario ar1",
        )
        self.assertEqual(result, "EXECUTION_CAPABLE_WORKFLOW_CANDIDATE")

    def test_artifact_upload_line_is_not_reclassified_by_runner_elsewhere(self):
        result, _ = classify(
            ".github/workflows/example.yml",
            "uses: actions/upload-artifact@v4",
        )
        self.assertEqual(result, "WORKFLOW_REFERENCE")

    def test_guard_line_is_control_path(self):
        result, _ = classify(
            ".github/workflows/example.yml",
            'raise SystemExit("BLOCKED: confirmatory execution is not authorized")',
        )
        self.assertEqual(result, "WORKFLOW_CONTROL_PATH")

    def test_compileall_reference_is_not_runner_invocation(self):
        result, _ = classify(
            ".github/workflows/scientific-validation.yml",
            "python -m compileall -q analysis/calibrate_null_type1_scenario.py",
        )
        self.assertEqual(result, "WORKFLOW_REFERENCE")

    def test_runner_token_is_a_discoverable_occurrence(self):
        self.assertTrue(_line_matches(
            "python -m analysis.calibrate_null_type1_scenario --scenario ar1"
        ))

    def test_generated_ledger_has_explicit_exclusion_reason(self):
        path = "protocol/TYPE1_V3_V4_OCCURRENCE_LEVEL_MANUAL_LEDGER_2026-10-31.json"
        self.assertIn(path, EXCLUDED_GENERATED_PATHS)
        self.assertTrue(EXCLUDED_GENERATED_PATHS[path])


    def test_governance_register_has_explicit_discovery_only_exclusion(self):
        path = "protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md"
        self.assertIn(path, EXCLUDED_GENERATED_PATHS)
        self.assertIn("self-referential", EXCLUDED_GENERATED_PATHS[path])
        self.assertIn("snapshot", EXCLUDED_GENERATED_PATHS[path])

    def test_inspect_ref_records_exclusion_without_scanning_ledger(self):
        generated = "protocol/TYPE1_V3_V4_OCCURRENCE_LEVEL_MANUAL_LEDGER_2026-10-31.json"
        register = "protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md"
        def fake_git(*args):
            if args[0] == "rev-parse":
                return "a" * 40
            if args[0] == "ls-tree":
                return generated + "\n" + register + "\n.github/workflows/example.yml"
            if args[0] == "show" and args[1].endswith(generated):
                return '{"V3": "V4", "confirmatory_execution_authorized": false}'
            if args[0] == "show" and args[1].endswith(register):
                return "V4 governance register; confirmatory_execution_authorized=false\n"
            if args[0] == "show" and args[1].endswith(".github/workflows/example.yml"):
                return "uses: actions/upload-artifact@v4\n"
            raise AssertionError(args)
        with patch("scripts.audit_type1_governance_refs.git", side_effect=fake_git):
            report = inspect_ref("HEAD")
        self.assertEqual(
            [row["path"] for row in report["excluded_paths"]],
            [generated, register],
        )
        self.assertNotIn(generated, [row["path"] for row in report["entries"]])
        self.assertNotIn(register, [row["path"] for row in report["entries"]])
        self.assertEqual(len(report["entries"]), 1)
        self.assertEqual(report["entries"][0]["matches"][0]["classification"], "WORKFLOW_REFERENCE")

    def test_governance_register_changes_trigger_inventory_workflow(self):
        from pathlib import Path
        workflow_path = Path(__file__).resolve().parents[1] / ".github/workflows/type1-v3-v4-governance-audit.yml"
        workflow = workflow_path.read_text(encoding="utf-8")
        self.assertIn('"protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md"', workflow)

    def test_occurrence_classifier_does_not_treat_runner_as_authority(self):
        result, note = classify(
            ".github/workflows/example.yml",
            "python -m analysis.calibrate_null_type1_scenario",
        )
        self.assertEqual(result, "EXECUTION_CAPABLE_WORKFLOW_CANDIDATE")
        self.assertIn("trace callers and guards", note)


if __name__ == "__main__":
    unittest.main(verbosity=2)
