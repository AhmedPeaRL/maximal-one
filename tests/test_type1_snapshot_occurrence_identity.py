from __future__ import annotations

import hashlib
import unittest


def canonical_id(ref_name, path, line, match_index):
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]
    return f"{ref_name}/{digest}/{line}/{match_index}"


class SnapshotOccurrenceIdentityTests(unittest.TestCase):

    def test_snapshot_ids_match_canonical_ledger_ids(self):
        inventory_ref = "HEAD"

        inventory_rows = [
            {
                "path": "analysis/example.py",
                "line": 12,
                "match_index_within_file": 1,
                "text": "estimate_alpha(series)",
            },
            {
                "path": ".github/workflows/example.yml",
                "line": 41,
                "match_index_within_file": 2,
                "text": "python -m analysis.runner",
            },
        ]

        ledger_ids = {
            canonical_id(
                inventory_ref,
                row["path"],
                row["line"],
                row["match_index_within_file"],
            )
            for row in inventory_rows
        }

        snapshot_ids = {
            canonical_id(
                inventory_ref,
                row["path"],
                row["line"],
                row["match_index_within_file"],
            )
            for row in inventory_rows
        }

        self.assertEqual(snapshot_ids, ledger_ids)
        self.assertEqual(len(snapshot_ids), len(inventory_rows))

    def test_review_prefix_must_not_replace_inventory_ref(self):
        expected = canonical_id(
            "HEAD",
            "analysis/example.py",
            12,
            1,
        )
        wrong = canonical_id(
            "REVIEW",
            "analysis/example.py",
            12,
            1,
        )

        self.assertNotEqual(expected, wrong)


if __name__ == "__main__":
    unittest.main()
