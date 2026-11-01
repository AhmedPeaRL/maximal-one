from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.generate_type1_occurrence_ledger import (
    INITIAL_FIELDS,
    build_ledger,
    generate,
    occurrence_id,
    reconcile_inventory_and_ledger,
    _validate_inventory,
)
from scripts.type1_occurrence_classifier import classify_occurrence

COMMIT = "a" * 40


def fixture_inventory() -> dict:
    return {
        "audit": "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1",
        "refs": [
            {
                "ref_requested": "HEAD",
                "commit_sha": COMMIT,
                "entries": [
                    {
                        "path": ".github/workflows/example.yml",
                        "matches": [
                            {
                                "line": 7,
                                "text": "workflow_dispatch:",
                                "classification": "WORKFLOW_REFERENCE",
                            },
                            {
                                "line": 11,
                                "text": "python runner.py",
                                "classification": "EXECUTION_CANDIDATE",
                            },
                        ],
                    },
                    {
                        "path": "analysis/example.py",
                        "matches": [
                            {
                                "line": 3,
                                "text": "ALPHA = 0.05",
                                "classification": "CODE_REFERENCE",
                            }
                        ],
                    },
                ],
            },
            {
                "ref_requested": "origin/main",
                "commit_sha": "b" * 40,
                "entries": [],
            },
        ],
    }


class OccurrenceLedgerTests(unittest.TestCase):
    def setUp(self):
        self.inventory = fixture_inventory()
        self.ref = _validate_inventory(self.inventory, COMMIT)

    def test_generates_one_row_per_source_occurrence(self):
        ledger = build_ledger(self.inventory, self.ref, "f" * 64)
        self.assertEqual(ledger["occurrence_count"], 3)
        self.assertEqual(len(ledger["records"]), 3)
        self.assertEqual(
            [row["occurrence_id"] for row in ledger["records"]],
            [
                occurrence_id("HEAD", ".github/workflows/example.yml", 7, 1),
                occurrence_id("HEAD", ".github/workflows/example.yml", 11, 2),
                occurrence_id("HEAD", "analysis/example.py", 3, 1),
            ],
        )

    def test_all_generated_rows_remain_unclassified_and_open(self):
        ledger = build_ledger(self.inventory, self.ref, "f" * 64)
        for row in ledger["records"]:
            for field, value in INITIAL_FIELDS.items():
                self.assertEqual(row[field], value)
        self.assertEqual(ledger["authority"], "DISCOVERY_TEMPLATE_ONLY_NOT_APPROVAL")

    def test_reconciliation_passes_exact_ledger(self):
        ledger = build_ledger(self.inventory, self.ref, "f" * 64)
        report = reconcile_inventory_and_ledger(self.inventory, self.ref, ledger)
        self.assertEqual(report["status"], "RECONCILED")
        self.assertEqual(report["expected_occurrence_count"], 3)
        self.assertEqual(report["missing_occurrence_ids"], [])
        self.assertEqual(report["extra_occurrence_ids"], [])

    def test_missing_occurrence_fails_reconciliation(self):
        ledger = build_ledger(self.inventory, self.ref, "f" * 64)
        ledger["records"].pop()
        ledger["occurrence_count"] -= 1
        report = reconcile_inventory_and_ledger(self.inventory, self.ref, ledger)
        self.assertEqual(report["status"], "RECONCILIATION_FAILED")
        self.assertEqual(len(report["missing_occurrence_ids"]), 1)

    def test_extra_occurrence_fails_reconciliation(self):
        ledger = build_ledger(self.inventory, self.ref, "f" * 64)
        extra = dict(ledger["records"][0])
        extra["occurrence_id"] = "HEAD/extra/999/1"
        ledger["records"].append(extra)
        ledger["occurrence_count"] += 1
        report = reconcile_inventory_and_ledger(self.inventory, self.ref, ledger)
        self.assertEqual(report["status"], "RECONCILIATION_FAILED")
        self.assertEqual(report["extra_occurrence_ids"], ["HEAD/extra/999/1"])

    def test_duplicate_occurrence_id_fails_reconciliation(self):
        ledger = build_ledger(self.inventory, self.ref, "f" * 64)
        ledger["records"].append(dict(ledger["records"][0]))
        ledger["occurrence_count"] += 1
        report = reconcile_inventory_and_ledger(self.inventory, self.ref, ledger)
        self.assertEqual(report["status"], "RECONCILIATION_FAILED")
        self.assertTrue(report["duplicate_occurrence_ids"])

    def test_source_identity_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly one inventory ref"):
            _validate_inventory(self.inventory, "c" * 40)

    def test_unsupported_inventory_schema_is_rejected(self):
        bad = dict(self.inventory)
        bad["audit"] = "UNRECOGNIZED"
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            _validate_inventory(bad, COMMIT)

    def test_path_traversal_is_rejected(self):
        bad = fixture_inventory()
        bad["refs"][0]["entries"][0]["path"] = "../outside.py"
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            _validate_inventory(bad, COMMIT)

    def test_line_number_must_be_positive_integer(self):
        bad = fixture_inventory()
        bad["refs"][0]["entries"][0]["matches"][0]["line"] = True
        with self.assertRaisesRegex(ValueError, "Invalid line number"):
            _validate_inventory(bad, COMMIT)

    def test_generation_writes_ledger_and_reconciliation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory_path = root / "inventory.json"
            ledger_path = root / "out" / "ledger.json"
            reconciliation_path = root / "out" / "reconciliation.json"
            inventory_path.write_text(json.dumps(self.inventory), encoding="utf-8")
            report = generate(
                inventory_path, COMMIT, ledger_path, reconciliation_path
            )
            self.assertEqual(report["status"], "RECONCILED")
            self.assertTrue(ledger_path.is_file())
            self.assertTrue(reconciliation_path.is_file())
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            self.assertEqual(ledger["inventory_sha256"], __import__("hashlib").sha256(inventory_path.read_bytes()).hexdigest())

    def test_manual_annotations_are_not_part_of_identity_projection(self):
        ledger = build_ledger(self.inventory, self.ref, "f" * 64)
        ledger["records"][0]["manual_classification"] = "DIAGNOSTIC"
        ledger["records"][0]["reviewer_disposition"] = "PENDING_SECOND_REVIEW"
        report = reconcile_inventory_and_ledger(self.inventory, self.ref, ledger)
        self.assertEqual(report["status"], "RECONCILED")

    def test_occurrence_local_assessment_is_added_without_manual_closure(self):
        self.inventory["refs"][0]["entries"][0]["matches"][0][
            "context_window"
        ] = [
            {"line": 6, "text": "Historical prior-run record."},
            {"line": 7, "text": "workflow_dispatch:"},
        ]

        ledger = build_ledger(self.inventory, self.ref, "f" * 64)

        row = next(
            item for item in ledger["records"]
            if item["line"] == 7
        )

        assessment = row["occurrence_local_assessment"]

        self.assertEqual(
            assessment["classifier"],
            "TYPE1_OCCURRENCE_LOCAL_CLASSIFIER_P1",
        )
        self.assertEqual(
            assessment["suggested_classification"],
            "HISTORICAL",
        )

        self.assertEqual(row["manual_classification"], "UNKNOWN")
        self.assertEqual(row["status"], "OPEN")
        self.assertEqual(row["reviewer_disposition"], "PENDING")


if __name__ == "__main__":
    unittest.main(verbosity=2)
