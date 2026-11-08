import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = json.loads((ROOT / "protocol" / "EVIDENCE_REGISTER_V3.json").read_text(encoding="utf-8"))
BATCH = json.loads((ROOT / "protocol" / "TYPE1_BATCH_REGISTER_V3_B001.json").read_text(encoding="utf-8"))
PROTOCOL = (ROOT / "protocol" / "TYPE1_MANUAL_OCCURRENCE_ADJUDICATION_PROTOCOL_V3.md").read_text(encoding="utf-8")

class EvidenceRegisterV3Tests(unittest.TestCase):
    def test_current_workflow_and_ci_identity(self):
        self.assertEqual(REGISTER["workflow_definition_commit"], "e3b65f622b6f03bfde82bdbddea403ef9e6d2d03")
        ci = REGISTER["v3_governance_ci"]
        self.assertEqual((ci["workflow_run_id"], ci["job_id"], ci["conclusion"], ci["tests_passed"]),
                         ("42419352067", "128544218446", "success", 21))

    def test_inventory_identity_and_counts(self):
        self.assertEqual(REGISTER["target"]["commit"], "e41fb7392b58198e8a4d8fa28b470b12b6ad2c31")
        self.assertEqual(REGISTER["target"]["occurrence_count"], 1711)
        self.assertEqual(REGISTER["main_comparison"]["commit"], "00bbd1fbd6df41b3e988ace75c480ea6232cfb86")
        self.assertEqual(REGISTER["main_comparison"]["occurrence_count"], 633)
        inv = REGISTER["inventory"]
        self.assertEqual((inv["workflow_run_id"], inv["artifact_id"]), ("42457774721", "13608356773"))
        self.assertEqual(inv["reference_inventory_sha256"], "5b4fbdca1bbdf56d47f38519fecf2b7cc325e3b41df2b9fe97dcd70cd9fd0b9a")
        for key in ("artifact_zip_sha256", "reference_inventory_sha256", "provenance_sha256"):
            self.assertRegex(inv[key], r"^[0-9a-f]{64}$")

    def test_target_snapshot_is_distinct_and_verified(self):
        snap = REGISTER["snapshot"]
        self.assertEqual((snap["workflow_run_id"], snap["artifact_id"]), ("42458102333", "13607909833"))
        self.assertEqual(snap["target_commit"], REGISTER["target"]["commit"])
        self.assertTrue(snap["extraction_verified"])
        self.assertEqual(snap["selected_file_count"], 264)
        self.assertEqual(snap["present_file_count"], 264)
        self.assertEqual(snap["extraction_checked_file_count"], 267)
        self.assertFalse(snap["v3_governance_implementation_included"])

    def test_governance_implementation_snapshot_is_separately_verified(self):
        gov = REGISTER["governance_implementation_snapshot"]
        self.assertEqual(gov["implementation_commit"], REGISTER["workflow_definition_commit"])
        self.assertEqual((gov["workflow_run_id"], gov["artifact_id"]), ("42419352220", "13592947197"))
        self.assertEqual(gov["status"], "VERIFIED")
        self.assertEqual(gov["file_count"], 13)
        self.assertTrue(gov["all_manifest_file_hashes_verified"])
        for key in ("artifact_zip_sha256", "manifest_sha256", "self_contained_implementation_zip_sha256"):
            self.assertRegex(gov[key], r"^[0-9a-f]{64}$")

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

    def test_protocol_has_current_evidence_and_no_stale_current_run_ids(self):
        self.assertIn("42457774721", PROTOCOL)
        self.assertIn("13608356773", PROTOCOL)
        self.assertIn("42458102333", PROTOCOL)
        self.assertIn("13607909833", PROTOCOL)
        self.assertIn("42419352220", PROTOCOL)
        self.assertIn("13592947197", PROTOCOL)
        for stale in ("785f3259bcda7529e9ce1b75186f881992259dda", "42412946073", "42413097084", "NOT_YET_CAPTURED"):
            self.assertNotIn(stale, PROTOCOL)
        self.assertIn("NOT_FROZEN", PROTOCOL)
        self.assertIn("promotion_authority = false", PROTOCOL)

if __name__ == "__main__":
    unittest.main()
