from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.merge_type1_manual_adjudication_overlay import (
    merge_overlay,
)


COMMIT = "a" * 40
SCHEMA = "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1"
OVERLAY_SCHEMA = "HCM_TYPE1_OCCURRENCE_MANUAL_ADJUDICATION_OVERLAY_V1"


class OverlayTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

        self.inventory_path = self.root / "inventory.json"
        self.ledger_path = self.root / "ledger.json"
        self.overlay_path = self.root / "overlay.json"
        self.output_path = self.root / "merged.json"

        self.inventory = {
            "audit": SCHEMA,
            "refs": [{
                "commit_sha": COMMIT,
                "ref_requested": "HEAD",
                "entries": [{
                    "path": "analysis/example.py",
                    "matches": [{
                        "line": 12,
                        "text": "example()",
                    }],
                }],
            }],
        }

        self.inventory_path.write_text(
            json.dumps(self.inventory),
            encoding="utf-8",
        )

        path_hash = hashlib.sha256(
            b"analysis/example.py"
        ).hexdigest()[:12]

        self.occurrence_id = f"HEAD/{path_hash}/12/1"

        self.ledger = {
            "inventory_commit": COMMIT,
            "inventory_ref": "HEAD",
            "inventory_sha256": self.inventory_sha(),
            "records": [{
                "occurrence_id": self.occurrence_id,
                "manual_classification": "UNKNOWN",
                "status": "OPEN",
                "reviewer_disposition": "PENDING",
                "closure_evidence": None,
            }],
        }

        self.ledger_path.write_text(
            json.dumps(self.ledger),
            encoding="utf-8",
        )

        self.overlay = {
            "schema": OVERLAY_SCHEMA,
            "review_commit_sha": COMMIT,
            "inventory_ref": "HEAD",
            "inventory_sha256": self.inventory_sha(),
            "records": [],
        }

    def tearDown(self):
        self.temp.cleanup()

    def inventory_sha(self):
        return hashlib.sha256(
            self.inventory_path.read_bytes()
        ).hexdigest()

    def write_overlay(self):
        self.overlay["inventory_sha256"] = self.inventory_sha()
        self.overlay_path.write_text(
            json.dumps(self.overlay),
            encoding="utf-8",
        )

    def run_merge(self):
        self.write_overlay()
        return merge_overlay(
            self.inventory_path,
            self.ledger_path,
            self.overlay_path,
            self.output_path,
        )

    def test_empty_overlay_preserves_unknown_open(self):
        result = self.run_merge()
        row = result["records"][0]

        self.assertEqual(row["manual_classification"], "UNKNOWN")
        self.assertEqual(row["status"], "OPEN")
        self.assertEqual(row["reviewer_disposition"], "PENDING")

    def test_human_decision_is_restored_after_regeneration(self):
        self.overlay["records"] = [{
            "occurrence_id": self.occurrence_id,
            "manual_classification": "EXECUTION_PATH",
            "status": "OPEN",
            "reviewer_disposition": "ADJUDICATED",
            "reviewer": "Human reviewer",
            "reviewed_at_utc": "2026-11-03T12:00:00Z",
            "rationale": "Direct caller confirmed from source and workflow trace.",
            "closure_evidence": None,
        }]

        first = self.run_merge()
        self.assertEqual(
            first["records"][0]["manual_classification"],
            "EXECUTION_PATH",
        )

        # Simulate a freshly regenerated ledger.
        self.ledger_path.write_text(
            json.dumps({
                **self.ledger,
                "records": [{
                    **self.ledger["records"][0],
                    "manual_classification": "UNKNOWN",
                    "status": "OPEN",
                    "reviewer_disposition": "PENDING",
                }],
            }),
            encoding="utf-8",
        )

        second = self.run_merge()
        self.assertEqual(
            second["records"][0]["manual_classification"],
            "EXECUTION_PATH",
        )

    def test_unknown_occurrence_id_is_rejected(self):
        self.overlay["records"] = [{
            "occurrence_id": "HEAD/not-in-inventory/1/1",
            "manual_classification": "EXECUTION_PATH",
            "status": "OPEN",
            "reviewer_disposition": "ADJUDICATED",
            "reviewer": "Reviewer",
            "reviewed_at_utc": "2026-11-03T12:00:00Z",
            "rationale": "Reviewed.",
            "closure_evidence": None,
        }]

        with self.assertRaisesRegex(ValueError, "Unknown occurrence ID"):
            self.run_merge()

    def test_duplicate_overlay_ids_are_rejected(self):
        row = {
            "occurrence_id": self.occurrence_id,
            "manual_classification": "EXECUTION_PATH",
            "status": "OPEN",
            "reviewer_disposition": "ADJUDICATED",
            "reviewer": "Reviewer",
            "reviewed_at_utc": "2026-11-03T12:00:00Z",
            "rationale": "Reviewed.",
            "closure_evidence": None,
        }

        self.overlay["records"] = [row, dict(row)]

        with self.assertRaisesRegex(ValueError, "Duplicate/conflicting"):
            self.run_merge()

    def test_closed_unknown_is_rejected(self):
        self.overlay["records"] = [{
            "occurrence_id": self.occurrence_id,
            "manual_classification": "UNKNOWN",
            "status": "CLOSED",
            "reviewer_disposition": "ADJUDICATED",
            "reviewer": "Reviewer",
            "reviewed_at_utc": "2026-11-03T12:00:00Z",
            "rationale": "Reviewed.",
            "closure_evidence": {
                "reference": "test.log",
                "description": "Evidence",
            },
        }]

        with self.assertRaisesRegex(ValueError, "UNKNOWN cannot be CLOSED"):
            self.run_merge()

    def test_closed_without_evidence_is_rejected(self):
        self.overlay["records"] = [{
            "occurrence_id": self.occurrence_id,
            "manual_classification": "DOCUMENTATION_REFERENCE",
            "status": "CLOSED",
            "reviewer_disposition": "ADJUDICATED",
            "reviewer": "Reviewer",
            "reviewed_at_utc": "2026-11-03T12:00:00Z",
            "rationale": "Reviewed.",
            "closure_evidence": None,
        }]

        with self.assertRaisesRegex(ValueError, "closure_evidence"):
            self.run_merge()

    def test_wrong_inventory_hash_is_rejected(self):
        self.write_overlay()

        corrupted = json.loads(
            self.overlay_path.read_text(encoding="utf-8")
        )
        corrupted["inventory_sha256"] = "0" * 64

        self.overlay_path.write_text(
            json.dumps(corrupted),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "SHA-256 mismatch",
        ):
            merge_overlay(
                self.inventory_path,
                self.ledger_path,
                self.overlay_path,
                self.output_path,
            )


if __name__ == "__main__":
    unittest.main()
