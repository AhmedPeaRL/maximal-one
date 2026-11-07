import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "scripts")
)

import merge_type1_manual_adjudication_overlay_v3 as merger


def make_record(**updates):
    record = {
        "occurrence_id": "refs/audit/target/aaaaaaaaaaaa/1/1",
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
        "test_run_job_artifact_commit": "run=1 job=2 artifact=3 commit=" + "a" * 40,
        "historical_diagnostic_proposed_governance_status": "current execution caller",
        "reviewer": "author-human-1",
        "reviewer_kind": "HUMAN",
        "reviewer_role": "repository author / primary reviewer",
        "conflict_statement": "Repository authorship disclosed",
        "reviewed_at_utc": "2026-11-07T12:00:00Z",
        "rationale": "Exact call path inspected",
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
            "rationale": "Awaiting independent human reviewer"
        }
    }

    record.update(updates)
    return record


class V3GovernanceTests(unittest.TestCase):

    def test_high_impact_open_pending_is_allowed(self):
        merger.validate_record(make_record())

    def test_high_impact_closed_pending_is_rejected(self):
        record = make_record(
            status="CLOSED",
            closure_evidence={
                "references": ["workflow.yml:L10"],
                "description": "Guard and negative test evidence",
                "negative_test_passed": True
            }
        )

        with self.assertRaises(ValueError):
            merger.validate_record(record)

    def test_same_person_cannot_be_second_reviewer(self):
        record = make_record(
            second_review={
                "status": "AGREED",
                "reviewer": "author-human-1",
                "reviewer_kind": "HUMAN",
                "reviewer_role": "reviewer",
                "conflict_statement": "Authorship disclosed",
                "reviewed_at_utc": "2026-11-07T13:00:00Z",
                "rationale": "Agree"
            }
        )

        with self.assertRaises(ValueError):
            merger.validate_record(record)

    def test_ai_cannot_be_second_reviewer(self):
        record = make_record(
            second_review={
                "status": "AGREED",
                "reviewer": "assistant",
                "reviewer_kind": "AI",
                "reviewer_role": "AI assistant",
                "conflict_statement": "AI system",
                "reviewed_at_utc": "2026-11-07T13:00:00Z",
                "rationale": "Agree"
            }
        )

        with self.assertRaises(ValueError):
            merger.validate_record(record)

    def test_distinct_human_agreement_allows_closure(self):
        record = make_record(
            status="CLOSED",
            closure_evidence={
                "references": [
                    "runner.py:L10-L20",
                    "test_wrong_branch.py::test_rejection"
                ],
                "description": "Full path and negative-test evidence",
                "negative_test_passed": True
            },
            second_review={
                "status": "AGREED",
                "reviewer": "independent-human-2",
                "reviewer_kind": "HUMAN",
                "reviewer_role": "independent reviewer",
                "conflict_statement": "No authorship or collaboration conflict",
                "reviewed_at_utc": "2026-11-07T13:00:00Z",
                "rationale": "Independently inspected and agreed"
            }
        )

        merger.validate_record(record)

    def test_disagreement_must_remain_open(self):
        record = make_record(
            status="CLOSED",
            closure_evidence={
                "references": ["source.py:L1"],
                "description": "Evidence",
                "negative_test_passed": True
            },
            second_review={
                "status": "DISAGREED",
                "reviewer": "independent-human-2",
                "reviewer_kind": "HUMAN",
                "reviewer_role": "reviewer",
                "conflict_statement": "None",
                "reviewed_at_utc": "2026-11-07T13:00:00Z",
                "rationale": "Disagree"
            }
        )

        with self.assertRaises(ValueError):
            merger.validate_record(record)

    def test_low_impact_can_use_not_required(self):
        record = make_record(
            manual_classification="DOCUMENTATION_ONLY",
            can_influence_execution="NO",
            second_review={
                "status": "NOT_REQUIRED",
                "reviewer": "",
                "reviewer_kind": "NONE",
                "reviewer_role": "",
                "conflict_statement": "",
                "reviewed_at_utc": "",
                "rationale": "Non-executable documentation occurrence"
            }
        )

        merger.validate_record(record)

    def test_ai_cannot_be_primary_reviewer(self):
        record = make_record(
            reviewer="assistant",
            reviewer_kind="AI"
        )

        with self.assertRaises(ValueError):
            merger.validate_record(record)

    def test_unresolved_cannot_be_closed(self):
        record = make_record(
            manual_classification="UNRESOLVED",
            can_influence_execution="UNRESOLVED",
            status="CLOSED",
            closure_evidence={
                "references": ["source.py:L1"],
                "description": "Evidence",
                "negative_test_passed": True
            },
            second_review={
                "status": "AGREED",
                "reviewer": "independent-human-2",
                "reviewer_kind": "HUMAN",
                "reviewer_role": "reviewer",
                "conflict_statement": "None",
                "reviewed_at_utc": "2026-11-07T13:00:00Z",
                "rationale": "Agree"
            }
        )

        with self.assertRaises(ValueError):
            merger.validate_record(record)


if __name__ == "__main__":
    unittest.main()
