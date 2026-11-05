import json, tempfile, unittest, hashlib, zipfile
from pathlib import Path
from scripts.create_type1_review_snapshot import (
    inventory_scanner_exclusions,
    load_inventory,
    safe_repo_path,
    select_snapshot_paths,
    create_self_contained_archive,
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
            _, paths, occurrences, inventory_ref = load_inventory(
                p,
                "a" * 40,
            )
        self.assertEqual(paths,["analysis/a.py","workflow/b.yml"])
        self.assertEqual(len(occurrences),2)
        self.assertEqual(inventory_ref, "HEAD")

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


    def test_governance_register_exclusion_remains_in_snapshot_scope(self):
        register = "protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md"
        exclusions = [{
            "path": register,
            "reason": "Self-referential governance register.",
            "handling": "EXCLUDED_FROM_OCCURRENCE_SCAN_RETAIN_IN_SNAPSHOT_SCOPE",
        }]
        selected = select_snapshot_paths(
            ["analysis/runner.py"],
            ["protocol/required.md"],
            exclusions,
        )
        self.assertIn(register, selected)
        self.assertIn("analysis/runner.py", selected)
        self.assertIn("protocol/required.md", selected)

    def test_governance_register_is_copied_and_hashed_in_snapshot_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            register = repo / "protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md"
            register.parent.mkdir(parents=True)
            payload = b"governance evidence register\n"
            register.write_bytes(payload)

            inventory = root / "inventory.json"
            ledger = root / "ledger.json"
            overlay = root / "overlay.json"
            for path in (inventory, ledger, overlay):
                path.write_text("{}\n", encoding="utf-8")

            archive, verification = create_self_contained_archive(
                repo_root=repo,
                selected_paths=["protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md"],
                inventory_path=inventory,
                ledger_path=ledger,
                overlay_path=overlay,
                output_dir=root / "snapshot",
            )
            self.assertTrue(verification["verified"])
            with zipfile.ZipFile(archive) as zipped:
                member = "source/repository/protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md"
                self.assertIn(member, zipped.namelist())
                self.assertEqual(zipped.read(member), payload)
                manifest = json.loads(zipped.read("manifest.json"))
                record = next(row for row in manifest["files"] if row["path"] == member)
                self.assertEqual(record["sha256"], hashlib.sha256(payload).hexdigest())

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
