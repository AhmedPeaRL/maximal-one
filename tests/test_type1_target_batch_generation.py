from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "adjudication/generate_target_batches.py"
TARGET_COMMIT = "ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876"
MAIN_COMMIT = "fe949fc4a11d245f08846d7eece97e8c1d26a3f8"
INVENTORY_SHA = "4e721c8dd55425c0d25dd043c3ec8433c4a4b96d1c11d6d4cb94acfaabb774b3"
RUN_ID = "43199940422"
ARTIFACT_ID = "13934996445"
ARTIFACT_NAME = "type1-v3-v4-governance-inventory-43199940422-1"
WORKFLOW_COMMIT = "2c228430b32b489d22e92298cc2edca6098acffb"


class TargetBatchGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory_path = self.root / "inventory.json"
        self.ledger_path = self.root / "occurrence_level_manual_ledger.json"
        self.main_ledger_path = self.root / "main_occurrence_level_manual_ledger.json"
        self.provenance_path = self.root / "provenance.json"
        self.artifact_path = self.root / "artifact.json"
        self.register_path = self.root / "population.json"
        self.output = self.root / "batches"
        self.records = [{
            "occurrence_id": f"refs/audit/target/test/{i}",
            "manual_classification": "UNKNOWN",
            "status": "OPEN",
            "reviewer_disposition": "PENDING",
        } for i in range(1800)]
        self.inventory_path.write_text(json.dumps({"fixture": "inventory"}), encoding="utf-8")
        self.main_ledger_path.write_text(json.dumps({"occurrence_count": 728}), encoding="utf-8")
        self.ledger_path.write_text(json.dumps({
            "inventory_commit": TARGET_COMMIT,
            "inventory_ref": "refs/audit/target",
            "inventory_sha256": hashlib.sha256(self.inventory_path.read_bytes()).hexdigest(),
            "occurrence_count": 1800,
            "records": self.records,
        }), encoding="utf-8")
        self.inv_sha = hashlib.sha256(self.inventory_path.read_bytes()).hexdigest()
        self.ledger_sha = hashlib.sha256(self.ledger_path.read_bytes()).hexdigest()
        self.main_sha = hashlib.sha256(self.main_ledger_path.read_bytes()).hexdigest()
        # Fixture hashes are deliberately used for unit tests; production values are enforced by V2 register.
        self.provenance_path.write_text(json.dumps({
            "workflow_run_id": RUN_ID,
            "target_commit": TARGET_COMMIT,
            "main_commit": MAIN_COMMIT,
            "workflow_definition_commit": WORKFLOW_COMMIT,
            "inventory_sha256": self.inv_sha,
        }), encoding="utf-8")
        self.artifact_path.write_text(json.dumps({
            "id": ARTIFACT_ID,
            "name": ARTIFACT_NAME,
            "digest": "sha256:" + "a" * 64,
            "expired": False,
            "workflow_run": {"id": RUN_ID},
        }), encoding="utf-8")
        self.write_register()

    def tearDown(self):
        self.temp.cleanup()

    def write_register(self):
        self.register_path.write_text(json.dumps({
            "target": {"commit": TARGET_COMMIT, "ref": "refs/audit/target", "occurrence_count": 1800},
            "main_comparison": {"commit": MAIN_COMMIT, "occurrence_count": 728},
            "inventory": {
                "workflow_run_id": RUN_ID,
                "artifact_id": ARTIFACT_ID,
                "artifact_name": ARTIFACT_NAME,
                "artifact_archive_sha256": "a" * 64,
                "reference_inventory_sha256": self.inv_sha,
                "target_ledger_sha256": self.ledger_sha,
                "main_ledger_sha256": self.main_sha,
                "workflow_definition_commit": WORKFLOW_COMMIT,
            },
        }), encoding="utf-8")

    def run_generator(self):
        return subprocess.run([
            sys.executable, str(SCRIPT),
            "--ledger", str(self.ledger_path),
            "--inventory", str(self.inventory_path),
            "--population-register", str(self.register_path),
            "--provenance", str(self.provenance_path),
            "--artifact-metadata", str(self.artifact_path),
            "--output", str(self.output),
        ], cwd=ROOT, text=True, capture_output=True, timeout=30, check=False)

    def mutate_register(self, section, key, value):
        data = json.loads(self.register_path.read_text())
        data[section][key] = value
        self.register_path.write_text(json.dumps(data), encoding="utf-8")

    def test_generates_72_batches_and_exact_1800_ids(self):
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        files = sorted(self.output.glob("BATCH_[0-9][0-9][0-9].json"))
        self.assertEqual(len(files), 72)
        register = json.loads((self.output / "BATCH_SET_REGISTER.json").read_text())
        self.assertEqual(register["source_inventory_workflow_run_id"], RUN_ID)
        self.assertEqual(register["source_inventory_artifact_id"], ARTIFACT_ID)
        observed = []
        for path in files:
            batch = json.loads(path.read_text())
            self.assertEqual(batch["authority"], "NONE")
            self.assertEqual(batch["count"], 25)
            self.assertFalse(batch["formal_calibration_authorized"])
            observed.extend(batch["occurrence_ids"])
        self.assertEqual(observed, [r["occurrence_id"] for r in self.records])
        self.assertEqual(len(set(observed)), 1800)

    def test_inventory_run_id_mismatch_blocks(self):
        self.mutate_register("inventory", "workflow_run_id", "42870936071")
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workflow run ID mismatch", result.stderr)
        self.assertFalse(self.output.exists())

    def test_inventory_artifact_id_mismatch_blocks(self):
        self.mutate_register("inventory", "artifact_id", "13789382482")
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("artifact ID mismatch", result.stderr)
        self.assertFalse(self.output.exists())

    def test_inventory_sha_mismatch_blocks(self):
        self.mutate_register("inventory", "reference_inventory_sha256", "0" * 64)
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("provenance inventory SHA mismatch", result.stderr)
        self.assertFalse(self.output.exists())

    def test_target_ledger_sha_mismatch_blocks(self):
        self.mutate_register("inventory", "target_ledger_sha256", "0" * 64)
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source ledger SHA-256 mismatch", result.stderr)
        self.assertFalse(self.output.exists())

    def test_duplicate_occurrence_id_blocks(self):
        self.records[-1]["occurrence_id"] = self.records[0]["occurrence_id"]
        self.ledger_path.write_text(json.dumps({
            "inventory_commit": TARGET_COMMIT, "inventory_ref": "refs/audit/target",
            "inventory_sha256": self.inv_sha, "occurrence_count": 1800, "records": self.records,
        }), encoding="utf-8")
        self.mutate_register("inventory", "target_ledger_sha256", hashlib.sha256(self.ledger_path.read_bytes()).hexdigest())
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate occurrence IDs", result.stderr)
        self.assertFalse(self.output.exists())

    def test_non_open_record_blocks(self):
        self.records[0]["status"] = "CLOSED"
        self.ledger_path.write_text(json.dumps({
            "inventory_commit": TARGET_COMMIT, "inventory_ref": "refs/audit/target",
            "inventory_sha256": self.inv_sha, "occurrence_count": 1800, "records": self.records,
        }), encoding="utf-8")
        self.mutate_register("inventory", "target_ledger_sha256", hashlib.sha256(self.ledger_path.read_bytes()).hexdigest())
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source record is not OPEN", result.stderr)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
