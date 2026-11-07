import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import merge_type1_manual_adjudication_overlay_v3 as merger

COMMIT = "e41fb7392b58198e8a4d8fa28b470b12b6ad2c31"
REF = "refs/audit/target"
PATH = ".github/workflows/example.yml"
PATH_HASH = hashlib.sha256(PATH.encode()).hexdigest()[:12]
OID1 = f"{REF}/{PATH_HASH}/10/1"
OID2 = f"{REF}/{PATH_HASH}/20/2"


def make_record(oid=OID1, **updates):
    record = {
        "occurrence_id": oid,
        "manual_classification": "EXECUTION_CALLER",
        "can_influence_execution": "YES",
        "direct_caller_or_workflow_step": "workflow job step",
        "indirect_call_path": "dispatch -> caller -> runner",
        "runner_entry_point_or_command": "python -m runner",
        "trigger_conditions_and_branch_restrictions": "review branch only",
        "matrix_and_protocol_consumed": "matrix.json",
        "authorization_guard_and_execution_order": "branch guard before runner",
        "guard_fails_closed": "YES",
        "negative_test": "wrong branch rejected before runner side effect",
        "test_run_job_artifact_commit": f"run=100 job=200 artifact=300 commit={COMMIT}",
        "historical_diagnostic_proposed_governance_status": "current execution caller",
        "reviewer": "ahmedpearl",
        "reviewer_kind": "HUMAN",
        "reviewer_role": "repository author / primary reviewer",
        "conflict_statement": "Repository authorship and intellectual interest disclosed",
        "reviewed_at_utc": "2026-11-07T12:00:00Z",
        "rationale": "Exact call path inspected against the frozen target snapshot",
        "status": "OPEN",
        "reviewer_disposition": "ADJUDICATED",
        "closure_evidence": None,
        "second_review": {
            "status": "PENDING",
            "reviewer": "",
            "reviewer_kind": "NONE",
            "reviewer_role": "",
            "conflict_statement": "",
            "reviewed_at_utc": "",
            "rationale": "Awaiting a distinct independent human reviewer",
        },
    }
    record.update(updates)
    return record


def agreed_second(reviewer="independent-reviewer"):
    return {
        "status": "AGREED",
        "reviewer": reviewer,
        "reviewer_kind": "HUMAN",
        "reviewer_role": "independent human reviewer",
        "conflict_statement": "No repository authorship or collaboration conflict declared",
        "reviewed_at_utc": "2026-11-07T14:00:00Z",
        "rationale": "Independently inspected source, caller path, guard order, and negative test",
    }


def closure_evidence():
    return {
        "references": [".github/workflows/example.yml:L1-L30", "tests/test_guard.py::test_wrong_branch"],
        "description": "Exact execution path, authorization order, and negative test evidence",
        "negative_test_passed": True,
        "negative_test_reference": "tests/test_guard.py::test_wrong_branch",
        "workflow_run_id": "42405484699",
        "workflow_job_id": "128502157954",
        "artifact_id": "13586499769",
        "commit_sha": COMMIT,
    }


class V3GovernanceAndIdentityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.inventory_path = self.root / "inventory.json"
        self.ledger_path = self.root / "ledger.json"
        self.overlay_path = self.root / "overlay.json"
        self.output_path = self.root / "merged.json"
        self.inventory = {
            "audit": "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1",
            "refs": [
                {
                    "ref_requested": REF,
                    "commit_sha": COMMIT,
                    "entries": [{
                        "path": PATH,
                        "matches": [{"line": 10, "text": "run: python"}, {"line": 20, "text": "uses: action"}],
                    }],
                },
                {
                    "ref_requested": "refs/audit/main",
                    "commit_sha": "0" * 40,
                    "entries": [{"path": "README.md", "matches": [{"line": 1, "text": "readme"}]}],
                },
            ],
        }
        self.write_inventory(self.inventory)
        self.ledger = {
            "schema": "HCM_TYPE1_OCCURRENCE_LEVEL_MANUAL_LEDGER_V1",
            "inventory_commit": COMMIT,
            "inventory_ref": REF,
            "inventory_sha256": self.inventory_sha(),
            "occurrence_count": 2,
            "records": [
                {"occurrence_id": OID1, "path": PATH, "line": 10, "commit_sha": COMMIT, "repository_ref": REF, "manual_classification": "UNKNOWN", "status": "OPEN"},
                {"occurrence_id": OID2, "path": PATH, "line": 20, "commit_sha": COMMIT, "repository_ref": REF, "manual_classification": "UNKNOWN", "status": "OPEN"},
            ],
        }
        self.write_ledger(self.ledger)
        self.overlay = {
            "schema": "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V3",
            "review_commit_sha": COMMIT,
            "inventory_ref": REF,
            "inventory_sha256": self.inventory_sha(),
            "records": [],
        }
        self.write_overlay(self.overlay)

    def tearDown(self):
        self.tmp.cleanup()

    def inventory_sha(self):
        return hashlib.sha256(self.inventory_path.read_bytes()).hexdigest()

    def write_inventory(self, value):
        self.inventory_path.write_text(json.dumps(value), encoding="utf-8")

    def write_ledger(self, value):
        self.ledger_path.write_text(json.dumps(value), encoding="utf-8")

    def write_overlay(self, value):
        self.overlay_path.write_text(json.dumps(value), encoding="utf-8")

    def run_merge(self):
        return merger.merge(self.inventory_path, self.ledger_path, self.overlay_path, self.output_path)

    def test_exact_inventory_and_ledger_identity_merge(self):
        result = self.run_merge()
        self.assertEqual(result["merged"], 2)
        merged = json.loads(self.output_path.read_text())
        self.assertEqual(merged["protocol_freeze"], "NOT_FROZEN")
        self.assertIs(merged["formal_calibration_authorized"], False)
        self.assertIs(merged["promotion_authority"], False)

    def test_overlay_inventory_hash_mismatch_rejected(self):
        self.overlay["inventory_sha256"] = "f" * 64
        self.write_overlay(self.overlay)
        with self.assertRaisesRegex(ValueError, "overlay inventory SHA-256 mismatch"):
            self.run_merge()

    def test_wrong_review_commit_rejected(self):
        self.overlay["review_commit_sha"] = "1" * 40
        self.write_overlay(self.overlay)
        with self.assertRaises(ValueError):
            self.run_merge()

    def test_wrong_inventory_ref_rejected(self):
        self.overlay["inventory_ref"] = "refs/audit/main"
        self.write_overlay(self.overlay)
        with self.assertRaises(ValueError):
            self.run_merge()

    def test_missing_ledger_occurrence_rejected(self):
        self.ledger["records"].pop()
        self.ledger["occurrence_count"] = 1
        self.write_ledger(self.ledger)
        with self.assertRaisesRegex(ValueError, "inventory/ledger ID set mismatch"):
            self.run_merge()

    def test_duplicate_ledger_occurrence_rejected(self):
        self.ledger["records"].append(dict(self.ledger["records"][0]))
        self.ledger["occurrence_count"] = 3
        self.write_ledger(self.ledger)
        with self.assertRaisesRegex(ValueError, "duplicate ledger occurrence ID"):
            self.run_merge()

    def test_ledger_path_line_identity_mismatch_rejected(self):
        self.ledger["records"][0]["path"] = "other.yml"
        self.write_ledger(self.ledger)
        with self.assertRaisesRegex(ValueError, "path/line mismatch"):
            self.run_merge()

    def test_overlay_unknown_id_rejected(self):
        self.overlay["records"] = [make_record("refs/audit/target/ffffffffffff/99/1")]
        self.write_overlay(self.overlay)
        with self.assertRaisesRegex(ValueError, "absent from verified inventory"):
            self.run_merge()

    def test_duplicate_overlay_id_rejected(self):
        self.overlay["records"] = [make_record(), make_record()]
        self.write_overlay(self.overlay)
        with self.assertRaisesRegex(ValueError, "duplicate overlay occurrence ID"):
            self.run_merge()

    def test_high_impact_open_pending_is_allowed(self):
        merger.validate_record(make_record(), expected_commit=COMMIT)

    def test_high_impact_closed_pending_is_rejected(self):
        record = make_record(status="CLOSED", closure_evidence=closure_evidence())
        with self.assertRaises(ValueError):
            merger.validate_record(record, expected_commit=COMMIT)

    def test_same_person_cannot_be_second_reviewer(self):
        record = make_record(second_review=agreed_second("AHMEDPEARL"))
        with self.assertRaisesRegex(ValueError, "distinct"):
            merger.validate_record(record, expected_commit=COMMIT)

    def test_ai_cannot_be_second_reviewer(self):
        second = agreed_second("assistant")
        second["reviewer_kind"] = "AI"
        record = make_record(second_review=second)
        with self.assertRaisesRegex(ValueError, "must be human"):
            merger.validate_record(record, expected_commit=COMMIT)

    def test_disagreement_must_remain_open(self):
        second = agreed_second("reviewer-2")
        second["status"] = "DISAGREED"
        record = make_record(status="CLOSED", closure_evidence=closure_evidence(), second_review=second)
        with self.assertRaises(ValueError):
            merger.validate_record(record, expected_commit=COMMIT)

    def test_unresolved_cannot_be_closed(self):
        record = make_record(
            manual_classification="UNRESOLVED",
            can_influence_execution="UNRESOLVED",
            status="CLOSED",
            closure_evidence=closure_evidence(),
            second_review=agreed_second("reviewer-2"),
        )
        with self.assertRaisesRegex(ValueError, "unresolved records cannot close"):
            merger.validate_record(record, expected_commit=COMMIT)

    def test_missing_negative_test_rejected(self):
        evidence = closure_evidence()
        evidence["negative_test_passed"] = False
        record = make_record(status="CLOSED", closure_evidence=evidence, second_review=agreed_second("reviewer-2"))
        with self.assertRaisesRegex(ValueError, "negative test must have passed"):
            merger.validate_record(record, expected_commit=COMMIT)

    def test_wrong_closure_commit_rejected(self):
        evidence = closure_evidence()
        evidence["commit_sha"] = "2" * 40
        record = make_record(status="CLOSED", closure_evidence=evidence, second_review=agreed_second("reviewer-2"))
        with self.assertRaisesRegex(ValueError, "does not match reviewed commit"):
            merger.validate_record(record, expected_commit=COMMIT)

    def test_distinct_human_agreement_allows_high_impact_closure(self):
        record = make_record(status="CLOSED", closure_evidence=closure_evidence(), second_review=agreed_second("reviewer-2"))
        merger.validate_record(record, expected_commit=COMMIT)

    def test_low_impact_not_required_is_allowed(self):
        second = {
            "status": "NOT_REQUIRED", "reviewer": "", "reviewer_kind": "NONE",
            "reviewer_role": "", "conflict_statement": "", "reviewed_at_utc": "",
            "rationale": "Documentation-only occurrence; no execution influence.",
        }
        record = make_record(manual_classification="DOCUMENTATION_ONLY", can_influence_execution="NO", second_review=second)
        merger.validate_record(record, expected_commit=COMMIT)

    def test_unresolved_influence_is_conservatively_high_impact(self):
        record = make_record(can_influence_execution="UNRESOLVED", manual_classification="DOCUMENTATION_ONLY")
        self.assertTrue(merger.high_impact(record))
        merger.validate_record(record, expected_commit=COMMIT)

    def test_json_schema_accepts_valid_overlay_and_rejects_missing_second_review(self):
        schema_path = Path(__file__).resolve().parents[1] / "protocol" / "TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V3.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        valid = {"schema": "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V3", "review_commit_sha": COMMIT, "inventory_ref": REF, "inventory_sha256": "a" * 64, "records": [make_record()]}
        self.assertEqual(list(validator.iter_errors(valid)), [])
        invalid = json.loads(json.dumps(valid))
        invalid["records"][0].pop("second_review")
        self.assertTrue(list(validator.iter_errors(invalid)))


if __name__ == "__main__":
    unittest.main()
