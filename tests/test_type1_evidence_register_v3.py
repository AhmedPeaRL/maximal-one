import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = json.loads((ROOT / "protocol" / "EVIDENCE_REGISTER_V3.json").read_text(encoding="utf-8"))
BATCH = json.loads((ROOT / "protocol" / "TYPE1_BATCH_REGISTER_V3_B001.json").read_text(encoding="utf-8"))
PROTOCOL = (ROOT / "protocol" / "TYPE1_MANUAL_OCCURRENCE_ADJUDICATION_PROTOCOL_V3.md").read_text(encoding="utf-8")
SNAPSHOT_WORKFLOW = (ROOT / ".github" / "workflows" / "type1-v3-governance-implementation-snapshot.yml").read_text(encoding="utf-8")

class EvidenceRegisterV3Tests(unittest.TestCase):
    def test_current_workflow_and_ci_identity(self):
        self.assertEqual(REGISTER["workflow_definition_commit"], "ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876")
        ci = REGISTER["v3_governance_ci"]
        self.assertEqual((ci["workflow_run_id"], ci["job_id"], ci["conclusion"], ci["tests_passed"]),
                         ("42496439182", "128779691121", "success", 28))
        self.assertEqual(ci["python_version"], "3.11.15")
        self.assertEqual(ci["schema_validator"], "jsonschema==4.26.0")

    def test_inventory_identity_and_counts(self):
        self.assertEqual(REGISTER["target"]["commit"], "e41fb7392b58198e8a4d8fa28b470b12b6ad2c31")
        self.assertEqual(REGISTER["target"]["occurrence_count"], 1711)
        self.assertEqual(REGISTER["main_comparison"]["commit"], "00bbd1fbd6df41b3e988ace75c480ea6232cfb86")
        self.assertEqual(REGISTER["main_comparison"]["occurrence_count"], 633)
        inv = REGISTER["inventory"]
        self.assertEqual((inv["workflow_run_id"], inv["artifact_id"]), ("42499309283", "13624359912"))
        self.assertEqual(inv["workflow_definition_commit"], REGISTER["workflow_definition_commit"])
        self.assertEqual(inv["reference_inventory_sha256"], "5b4fbdca1bbdf56d47f38519fecf2b7cc325e3b41df2b9fe97dcd70cd9fd0b9a")
        self.assertEqual(inv["provenance_sha256"], "6835bedf923142231d76a52874ce3fad5327508f4f95d955a215962c597d318b")
        self.assertEqual(inv["target_commit"], REGISTER["target"]["commit"])
        for key in ("artifact_zip_sha256", "reference_inventory_sha256", "provenance_sha256"):
            self.assertRegex(inv[key], r"^[0-9a-f]{64}$")

    def test_target_snapshot_is_distinct_and_verified(self):
        snap = REGISTER["snapshot"]
        self.assertEqual((snap["workflow_run_id"], snap["artifact_id"]), ("42499453986", "13624771675"))
        self.assertEqual(snap["target_commit"], REGISTER["target"]["commit"])
        self.assertEqual(snap["inventory_source_commit"], REGISTER["target"]["commit"])
        self.assertTrue(snap["extraction_verified"])
        self.assertEqual(snap["selected_file_count"], 264)
        self.assertEqual(snap["present_file_count"], 264)
        self.assertEqual(snap["extraction_checked_file_count"], 267)
        self.assertFalse(snap["v3_governance_implementation_included"])

    def test_governance_implementation_snapshot_is_separately_verified(self):
        gov = REGISTER["governance_implementation_snapshot"]
        self.assertEqual(gov["implementation_commit"], REGISTER["workflow_definition_commit"])
        self.assertEqual((gov["workflow_run_id"], gov["artifact_id"]), ("42496227821", "13623039718"))
        self.assertEqual(gov["status"], "VERIFIED")
        self.assertEqual(gov["file_count"], 13)
        self.assertTrue(gov["all_manifest_file_hashes_verified"])
        self.assertFalse(gov["batch_register_included"])
        self.assertFalse(gov["new_evidence_test_included"])
        for key in ("artifact_zip_sha256", "manifest_sha256", "self_contained_implementation_zip_sha256"):
            self.assertRegex(gov[key], r"^[0-9a-f]{64}$")

    def test_branch_divergence_is_recorded_without_merge_authority(self):
        relation = REGISTER["branch_relation_to_main"]
        self.assertEqual(relation["status"], "diverged")
        self.assertEqual((relation["review_ahead_by"], relation["review_behind_by"]), (330, 19))
        self.assertIn("Do not merge the entire review branch", relation["decision"])

    def test_non_authority_invariants(self):
        self.assertEqual(REGISTER["protocol_freeze"], "NOT_FROZEN")
        for key in ("formal_calibration_authorized", "confirmatory_execution_authorized", "claim_support", "promotion_authority"):
            self.assertIs(REGISTER[key], False)
        self.assertEqual(REGISTER["manual_adjudication_overlay_records"], 0)

    def test_batch_is_new_navigation_only_sequence_bound_to_current_inventory(self):
        self.assertEqual(BATCH["status"], "NAVIGATION_ONLY_NOT_ADJUDICATED")
        self.assertEqual(BATCH["target_commit"], REGISTER["target"]["commit"])
        self.assertEqual(BATCH["inventory_sha256"], REGISTER["inventory"]["reference_inventory_sha256"])
        ids = BATCH["occurrence_ids"]
        self.assertEqual(len(ids), 25)
        self.assertEqual(len(set(ids)), 25)
        self.assertEqual(BATCH["count"], 25)
        self.assertEqual(BATCH["first_occurrence_id"], ids[0])
        self.assertEqual(BATCH["last_occurrence_id"], ids[-1])
        digest = hashlib.sha256(("\n".join(ids) + "\n").encode("utf-8")).hexdigest()
        self.assertEqual(digest, BATCH["canonical_id_sequence_sha256"])
        self.assertEqual(digest, "a65ca1bff93f8ea841f6b46b9fb87cb3fe2827299ea5d7632ea3a0fa679f576b")
        self.assertEqual(BATCH["authority"], "NONE")
        self.assertEqual(BATCH["protocol_freeze"], "NOT_FROZEN")

    def test_v4_review_handoff_requires_same_commit_inventory_and_snapshot(self):
        handoff = REGISTER["v4_statistical_review_handoff"]
        self.assertEqual(handoff["status"], "BLOCKED_PENDING_EXACT_AD106_INVENTORY_AND_REVIEW_SNAPSHOT")
        self.assertEqual(handoff["required_inventory_target_commit"], handoff["candidate_review_commit"])
        self.assertEqual(handoff["required_review_snapshot_commit"], handoff["candidate_review_commit"])
        self.assertNotEqual(handoff["current_inventory_source_commit"], handoff["candidate_review_commit"])
        self.assertNotEqual(handoff["current_snapshot_review_commit"], handoff["candidate_review_commit"])

    def test_snapshot_workflow_captures_all_governance_inputs(self):
        required_paths = (
            "protocol/TYPE1_BATCH_REGISTER_V3_B001.json",
            "tests/test_type1_evidence_register_v3.py",
            "scripts/audit_type1_governance_refs.py",
            "tests/test_type1_governance_binary_scan.py",
            "tests/test_type1_governance_generated_exclusions.py",
        )
        for path in required_paths:
            self.assertGreaterEqual(SNAPSHOT_WORKFLOW.count(path), 2)

    def test_protocol_has_current_evidence_and_no_stale_current_run_ids(self):
        for current in ("42496439182", "42499309283", "13624359912", "42499453986", "13624771675", "42496227821", "13623039718"):
            self.assertIn(current, PROTOCOL)
        for stale in ("42419352067", "42457774721", "42458102333", "42419352220", "13592947197", "785f3259bcda7529e9ce1b75186f881992259dda"):
            self.assertNotIn(stale, PROTOCOL)
        self.assertIn("NOT_FROZEN", PROTOCOL)
        self.assertIn("promotion_authority = false", PROTOCOL)

if __name__ == "__main__":
    unittest.main()
