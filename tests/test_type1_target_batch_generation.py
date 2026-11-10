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
INVENTORY_SHA = "b30db3cb254f276a6d2707cbdbc4bef06f1dad92c4063c7098eedaae84154c92"


class TargetBatchGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger_path = self.root / "ledger.json"
        self.register_path = self.root / "population.json"
        self.output = self.root / "batches"
        self.records = [
            {
                "occurrence_id": f"refs/audit/target/test/{i}",
                "manual_classification": "UNKNOWN",
                "status": "OPEN",
                "reviewer_disposition": "PENDING",
            }
            for i in range(1800)
        ]
        self.write_fixture()

    def tearDown(self):
        self.temp.cleanup()

    def write_fixture(self):
        ledger = {
            "inventory_commit": TARGET_COMMIT,
            "inventory_ref": "refs/audit/target",
            "inventory_sha256": INVENTORY_SHA,
            "occurrence_count": 1800,
            "records": self.records,
        }
        self.ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
        self.register_path.write_text(
            json.dumps(
                {
                    "target": {
                        "commit": TARGET_COMMIT,
                        "ref": "refs/audit/target",
                        "occurrence_count": 1800,
                    },
                    "inventory": {
                        "reference_inventory_sha256": INVENTORY_SHA,
                        "target_ledger_sha256": hashlib.sha256(
                            self.ledger_path.read_bytes()
                        ).hexdigest(),
                        "workflow_run_id": "42870936071",
                        "artifact_id": "13789382482",
                        "workflow_definition_commit": "4d0fe317ff8e20cdd7f1767e31215d958d87508b",
                    },
                }
            ),
            encoding="utf-8",
        )

    def run_generator(self):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--ledger",
                str(self.ledger_path),
                "--population-register",
                str(self.register_path),
                "--output",
                str(self.output),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )

    def test_generates_72_batches_and_exact_1800_ids(self):
        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        files = sorted(self.output.glob("BATCH_[0-9][0-9][0-9].json"))
        self.assertEqual(len(files), 72)
        register = json.loads((self.output / "BATCH_SET_REGISTER.json").read_text())
        self.assertEqual(register["inventory_sha256"], INVENTORY_SHA)
        self.assertEqual(register["source_ledger_sha256"], hashlib.sha256(self.ledger_path.read_bytes()).hexdigest())
        observed = []
        for path in files:
            batch = json.loads(path.read_text())
            self.assertEqual(batch["status"], "NAVIGATION_ONLY_NOT_ADJUDICATED")
            self.assertEqual(batch["authority"], "NONE")
            self.assertEqual(batch["count"], 25)
            observed.extend(batch["occurrence_ids"])
        self.assertEqual(observed, [r["occurrence_id"] for r in self.records])
        self.assertEqual(len(set(observed)), 1800)

    def test_wrong_inventory_hash_blocks_before_output(self):
        data = json.loads(self.register_path.read_text())
        data["inventory"]["reference_inventory_sha256"] = "0" * 64
        self.register_path.write_text(json.dumps(data))
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_wrong_source_ledger_hash_blocks_before_output(self):
        data = json.loads(self.register_path.read_text())
        data["inventory"]["target_ledger_sha256"] = "0" * 64
        self.register_path.write_text(json.dumps(data))
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_duplicate_occurrence_id_blocks_before_output(self):
        self.records[-1]["occurrence_id"] = self.records[0]["occurrence_id"]
        self.write_fixture()
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_non_open_record_blocks_before_output(self):
        self.records[0]["status"] = "CLOSED"
        self.write_fixture()
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_existing_output_directory_is_not_overwritten(self):
        self.output.mkdir()
        marker = self.output / "preserve.txt"
        marker.write_text("do not overwrite")
        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(marker.read_text(), "do not overwrite")


if __name__ == "__main__":
    unittest.main(verbosity=2)
