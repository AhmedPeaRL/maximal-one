from __future__ import annotations

import unittest

from scripts.generate_type1_occurrence_ledger import (
    build_ledger,
)
from scripts.create_type1_review_snapshot import (
    build_snapshot_occurrence_rows,
)


class SnapshotOccurrenceIdentityTests(unittest.TestCase):

    def test_snapshot_ids_match_actual_generated_ledger(self):
        commit = "a" * 40

        inventory = {
            "audit": (
                "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1"
            ),
            "refs": [{
                "ref_requested": "HEAD",
                "commit_sha": commit,
                "entries": [
                    {
                        "path": "analysis/example.py",
                        "matches": [
                            {
                                "line": 12,
                                "text": "estimate_alpha(series)",
                                "classification": "CODE",
                            },
                            {
                                "line": 19,
                                "text": "parametric_short_memory_null(x)",
                                "classification": "CODE",
                            },
                        ],
                    },
                    {
                        "path": ".github/workflows/example.yml",
                        "matches": [
                            {
                                "line": 41,
                                "text": "python -m analysis.runner",
                                "classification": "WORKFLOW",
                            },
                        ],
                    },
                ],
            }],
        }

        ref = inventory["refs"][0]

        ledger = build_ledger(
            inventory,
            ref,
            "b" * 64,
        )

        occurrences = []

        for entry in ref["entries"]:
            for index, match in enumerate(
                entry["matches"],
                1,
            ):
                occurrences.append({
                    "path": entry["path"],
                    "line": match["line"],
                    "match_index_within_file": index,
                    "text": match["text"],
                    "automated_classification": (
                        match["classification"]
                    ),
                    "automated_note": "",
                })

        snapshot_rows = build_snapshot_occurrence_rows(
            occurrences,
            ref["ref_requested"],
        )

        ledger_by_id = {
            row["occurrence_id"]: row
            for row in ledger["records"]
        }

        snapshot_by_id = {
            row["occurrence_id"]: row
            for row in snapshot_rows
        }

        self.assertEqual(
            set(snapshot_by_id),
            set(ledger_by_id),
        )

        self.assertEqual(
            len(snapshot_by_id),
            len(snapshot_rows),
        )

        for oid, snapshot_row in snapshot_by_id.items():
            ledger_row = ledger_by_id[oid]

            self.assertEqual(
                snapshot_row["path"],
                ledger_row["path"],
            )

            self.assertEqual(
                snapshot_row["line"],
                ledger_row["line"],
            )

            self.assertEqual(
                snapshot_row["text"],
                ledger_row["exact_matched_text"],
            )

            self.assertEqual(
                snapshot_row["manual_classification"],
                "UNKNOWN",
            )

            self.assertEqual(
                snapshot_row["status"],
                "OPEN",
            )


if __name__ == "__main__":
    unittest.main()
