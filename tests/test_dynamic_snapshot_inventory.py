import json, tempfile, unittest
from pathlib import Path
from scripts.create_type1_review_snapshot import (
    inventory_scanner_exclusions,
    load_inventory,
    safe_repo_path,
)

class InventoryScopeTests(unittest.TestCase):
    def test_all_inventory_paths_are_returned(self):
        data={"audit":"TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1","refs":[
            {"ref_requested":"HEAD","commit_sha":"a"*40,"entries":[
                {"path":"analysis/a.py","matches":[{"line":2,"text":"V4","classification":"CODE"}]},
                {"path":"workflow/b.yml","matches":[{"line":4,"text":"V3","classification":"WORKFLOW"}]}
            ]}
        ]}
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"inventory.json"; p.write_text(json.dumps(data))
            _, paths, occurrences=load_inventory(p,"a"*40)
        self.assertEqual(paths,["analysis/a.py","workflow/b.yml"])
        self.assertEqual(len(occurrences),2)

    def test_commit_mismatch_blocks(self):
        data={"audit":"TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1","refs":[
            {"ref_requested":"HEAD","commit_sha":"b"*40,"entries":[{"path":"a.py","matches":[]}]}
        ]}
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"inventory.json"; p.write_text(json.dumps(data))
            with self.assertRaises(SystemExit):
                load_inventory(p,"a"*40)

    def test_path_traversal_blocks(self):
        with self.assertRaises(SystemExit):
            safe_repo_path("../outside.txt")

    def test_scanner_exclusions_are_explicit_and_preserved(self):
        data = {
            "audit": "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1",
            "refs": [{
                "ref_requested": "HEAD",
                "commit_sha": "a" * 40,
                "entries": [],
                "excluded_paths": [{
                    "path": "protocol/generated-ledger.json",
                    "reason": "Generated evidence; do not recursively scan.",
                    "handling": "EXCLUDED_FROM_OCCURRENCE_SCAN_RETAIN_IN_SNAPSHOT_SCOPE",
                }],
            }],
        }
        rows = inventory_scanner_exclusions(data, "a" * 40)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["path"], "protocol/generated-ledger.json")
        self.assertIn("RETAIN_IN_SNAPSHOT_SCOPE", rows[0]["handling"])

    def test_malformed_scanner_exclusion_blocks(self):
        data = {
            "audit": "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1",
            "refs": [{
                "ref_requested": "HEAD",
                "commit_sha": "a" * 40,
                "entries": [],
                "excluded_paths": [{"path": "protocol/generated-ledger.json"}],
            }],
        }
        with self.assertRaises(SystemExit):
            inventory_scanner_exclusions(data, "a" * 40)

    def test_scanner_exclusion_path_traversal_blocks(self):
        data = {
            "audit": "TYPE1_V3_V4_THRESHOLD_REFERENCE_INVENTORY_V1",
            "refs": [{
                "ref_requested": "HEAD",
                "commit_sha": "a" * 40,
                "entries": [],
                "excluded_paths": [{
                    "path": "../outside.json",
                    "reason": "test",
                    "handling": "test",
                }],
            }],
        }
        with self.assertRaises(SystemExit):
            inventory_scanner_exclusions(data, "a" * 40)

if __name__=="__main__":
    unittest.main()
