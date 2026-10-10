import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

import analysis.audit_secondary_monthly_domains as audit
from analysis.acquire_secondary_domain_snapshots import ANALYSIS_END, SOURCES, parse_hadcet, parse_fred_indpro


class SecondaryAcquisitionSafetyTests(unittest.TestCase):
    def test_hadcet_missing_sentinel_is_not_numeric(self):
        # Twelve monthly cells plus annual summary; three months are missing.
        data = b"2025 1.0 2.0 -99.9 4.0 -99.9 6.0 7.0 8.0 -99.9 10.0 11.0 12.0 5.0\n2026 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0 12.0 7.0\n"
        rows = parse_hadcet(data)
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[-1]["date"], ANALYSIS_END)
        self.assertEqual([r["date"] for r in rows if not r["value"]], ["2025-03-01", "2025-05-01", "2025-09-01"])
        self.assertNotIn("-99.9", [r["value"] for r in rows])

    def test_hadcet_fixed_cutoff_excludes_future_year(self):
        data = b"2025 1 2 3 4 5 6 7 8 9 10 11 12 6\n2026 1 2 3 4 5 6 7 8 9 10 11 12 6\n"
        rows = parse_hadcet(data)
        self.assertEqual(rows[-1]["date"], "2025-12-01")

    def test_fred_fixed_cutoff_excludes_future_year(self):
        data = b"observation_date,INDPRO\n2025-11-01,100\n2025-12-01,101\n2026-01-01,102\n"
        rows = parse_fred_indpro(data)
        self.assertEqual([r["date"] for r in rows], ["2025-11-01", "2025-12-01"])

    def test_fred_first_url_is_bounded_to_frozen_window(self):
        first_url = SOURCES["fred_indpro"]["urls"][0]
        self.assertIn("cosd=1919-01-01", first_url)
        self.assertIn("coed=2025-12-01", first_url)

    def test_calibration_workflow_uses_module_invocation(self):
        workflow = Path(".github/workflows/null-type1-calibration.yml").read_text(encoding="utf-8")
        self.assertIn("python -m analysis.calibrate_null_type1_scenario", workflow)
        self.assertNotIn("python analysis/calibrate_null_type1_scenario.py", workflow)

    def test_integrity_audit_blocks_missing_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw.txt"
            raw.write_bytes(b"synthetic raw snapshot")
            parsed = root / "parsed.csv"
            # 1024 consecutive months ending at the frozen cutoff.
            end = 2025 * 12 + 11
            start = end - 1023
            rows = []
            for i in range(1024):
                month_index = start + i
                year = month_index // 12
                month = month_index % 12 + 1
                value = "" if i == 100 else "10.0"
                rows.append({"date": f"{year:04d}-{month:02d}-01", "value": value})
            with parsed.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["date", "value"], lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            manifest = {"sources": {"hadcet_monthly": {
                "raw_snapshot_path": "raw.txt",
                "raw_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
                "parsed_sha256": hashlib.sha256(parsed.read_bytes()).hexdigest(),
            }}}
            old_root = audit.ROOT
            try:
                audit.ROOT = root
                result = audit.audit_one("hadcet_monthly", parsed, manifest)
            finally:
                audit.ROOT = old_root
            self.assertFalse(result["time_integrity_passed"])
            self.assertEqual(result["missing_or_nonfinite_rows"], 1)
            self.assertTrue(any("missing_or_nonfinite_value" in x for x in result["failure_reasons"]))


if __name__ == "__main__":
    unittest.main()
