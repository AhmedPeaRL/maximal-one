from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "adjudication/generate_target_batches.py"

TARGET_COMMIT = (
    "ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876"
)
INVENTORY_SHA = (
    "88222e3178bc62854ffb8d1fa961c1fb4cfe582c9ff1082878ab759e011cc635"
)


class TargetBatchGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "evidence").mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def make_ledger(self):
        records = [
            {
                "occurrence_id": f"refs/audit/target/test/{i}",
                "manual_classification": "UNKNOWN",
                "status": "OPEN",
                "reviewer_disposition": "PENDING",
            }
            for i in range(1800)
        ]

        ledger = {
            "inventory_commit": TARGET_COMMIT,
            "inventory_ref": "refs/audit/target",
            "inventory_sha256": INVENTORY_SHA,
            "occurrence_count": 1800,
            "records": records,
        }

        path = (
            self.root
            / "evidence/occurrence_level_manual_ledger.json"
        )
        path.write_text(
            json.dumps(ledger),
            encoding="utf-8",
        )
        return ledger

    def run_generator(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )

    def test_generates_exactly_72_batches(self):
        ledger = self.make_ledger()

        result = self.run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)

        out = self.root / "adjudication/target_1800_batches"
        files = sorted(out.glob("BATCH_[0-9][0-9][0-9].json"))

        self.assertEqual(len(files), 72)

        register = json.loads(
            (out / "BATCH_SET_REGISTER.json").read_text()
        )

        self.assertEqual(len(register["batches"]), 72)
        self.assertEqual(register["expected_occurrences"], 1800)

        observed = []
        for path in files:
            batch = json.loads(path.read_text())
            self.assertEqual(
                batch["status"],
                "NAVIGATION_ONLY_NOT_ADJUDICATED",
            )
            self.assertEqual(batch["authority"], "NONE")
            observed.extend(batch["occurrence_ids"])

        expected = [
            row["occurrence_id"]
            for row in ledger["records"]
        ]

        self.assertEqual(observed, expected)
        self.assertEqual(len(set(observed)), 1800)

    def test_wrong_inventory_hash_blocks_before_output(self):
        ledger = self.make_ledger()
        ledger["inventory_sha256"] = "0" * 64

        (self.root / "evidence/occurrence_level_manual_ledger.json").write_text(
            json.dumps(ledger),
            encoding="utf-8",
        )

        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)

        self.assertFalse(
            (self.root / "adjudication/target_1800_batches").exists()
        )

    def test_duplicate_occurrence_id_blocks_before_output(self):
        ledger = self.make_ledger()
        ledger["records"][-1]["occurrence_id"] = (
            ledger["records"][0]["occurrence_id"]
        )

        (self.root / "evidence/occurrence_level_manual_ledger.json").write_text(
            json.dumps(ledger),
            encoding="utf-8",
        )

        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)

        self.assertFalse(
            (self.root / "adjudication/target_1800_batches").exists()
        )

    def test_non_open_record_blocks_before_output(self):
        ledger = self.make_ledger()
        ledger["records"][0]["status"] = "CLOSED"

        (self.root / "evidence/occurrence_level_manual_ledger.json").write_text(
            json.dumps(ledger),
            encoding="utf-8",
        )

        result = self.run_generator()
        self.assertNotEqual(result.returncode, 0)

        self.assertFalse(
            (self.root / "adjudication/target_1800_batches").exists()
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
