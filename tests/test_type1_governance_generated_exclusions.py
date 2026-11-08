from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.audit_type1_governance_refs import EXCLUDED_GENERATED_PATHS

EXPECTED_GENERATED_PATHS = {
    "evidence/CURRENT_EVIDENCE_REGISTER.json",
    "evidence/main_occurrence_level_manual_ledger.json",
    "evidence/occurrence_level_manual_ledger.json",
    "evidence/provenance.json",
    "evidence/reference_inventory.json",
    "evidence/snapshot_manifest.json",
    "evidence/three_way_identity_certificate.json",
    "adjudication/review_1711_e41fb_adjudication_template.csv",
    "adjudication/main_583_fe0d_adjudication_template.csv",
}


class GeneratedEvidenceExclusionTests(unittest.TestCase):
    def test_all_known_generated_outputs_are_explicitly_excluded(self):
        self.assertTrue(EXPECTED_GENERATED_PATHS.issubset(EXCLUDED_GENERATED_PATHS))

    def test_generated_files_are_reported_but_not_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            scanner_source = Path(__file__).resolve().parents[1] / "scripts" / "audit_type1_governance_refs.py"
            shutil.copy2(scanner_source, root / "scripts" / "audit_type1_governance_refs.py")

            for rel in EXPECTED_GENERATED_PATHS:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("V4 confirmatory_execution_authorized BLOCKED\n", encoding="utf-8")

            ordinary = root / "analysis" / "real_source.py"
            ordinary.parent.mkdir(parents=True)
            ordinary.write_text("V4 confirmatory_execution_authorized = False\n", encoding="utf-8")

            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Governance Test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "governance-test@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)

            env = os.environ.copy()
            env["GIT_CONFIG_NOSYSTEM"] = "1"
            subprocess.run(
                [sys.executable, "scripts/audit_type1_governance_refs.py", "HEAD"],
                cwd=root,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            report_path = root / "artifacts/type1_governance_inventory/reference_inventory.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            ref = report["refs"][0]
            excluded = {row["path"]: row["handling"] for row in ref["excluded_paths"]}
            entries = {row["path"] for row in ref["entries"]}

            for rel in EXPECTED_GENERATED_PATHS:
                self.assertEqual(
                    excluded.get(rel),
                    "EXCLUDED_FROM_OCCURRENCE_SCAN_RETAIN_IN_SNAPSHOT_SCOPE",
                    rel,
                )
                self.assertNotIn(rel, entries)
            self.assertIn("analysis/real_source.py", entries)


if __name__ == "__main__":
    unittest.main()
