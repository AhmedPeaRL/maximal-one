import csv
import hashlib
import io
import unittest

from analysis.prospective_raw_audit import (
    AUDIT_END,
    MIN_REPLICATION_OBSERVATIONS,
    parse_fred_cpiaucns,
    parse_hadukp,
    sha256_bytes,
    write_parsed,
    structural_audit,
)


class ProspectiveRawAuditTests(unittest.TestCase):
    def test_hadukp_parser_ignores_annual_summary_and_converts_sentinel_to_missing(self):
        raw = b"header\n 2025 1 2 -99.9 4 5 6 7 8 9 10 11 12 78\n 2026 2 3 4 5 6 7 8 9 10 11 12 13 90\n"
        rows = parse_hadukp(raw)
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[2]["date"], "2025-03-01")
        self.assertEqual(rows[2]["value"], "")
        self.assertEqual(rows[-1]["date"], AUDIT_END)
        self.assertNotIn("78", [row["value"] for row in rows])

    def test_fred_parser_respects_frozen_window(self):
        raw = b"observation_date,CPIAUCNS\n1913-01-01,9.8\n2025-12-01,320\n2026-01-01,321\n"
        rows = parse_fred_cpiaucns(raw)
        self.assertEqual([r["date"] for r in rows], ["1913-01-01", "2025-12-01"])

    def test_raw_hash_is_byte_hash_and_not_parsed_hash(self):
        raw = b"observation_date,CPIAUCNS\r\n1913-01-01,9.8\r\n"
        parsed = parse_fred_cpiaucns(raw)
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=["date", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(parsed)
        self.assertEqual(sha256_bytes(raw), hashlib.sha256(raw).hexdigest())
        self.assertNotEqual(sha256_bytes(raw), sha256_bytes(out.getvalue().encode()))

    def test_missingness_and_gaps_block_structural_eligibility(self):
        rows = []
        # 1024 monthly rows but one missing value; create an explicit gap too.
        start = 1913 * 12 + 1
        for i in range(MIN_REPLICATION_OBSERVATIONS):
            idx = start + i + (1 if i >= 300 else 0)
            year, month0 = divmod(idx, 12)
            date = f"{year:04d}-{month0 + 1:02d}-01"
            rows.append({"date": date, "value": "" if i == 20 else "1.0"})
        result = structural_audit(rows)
        self.assertEqual(result["missing_or_nonfinite_value_count"], 1)
        self.assertFalse(result["structural_checks"]["all_values_present_and_finite"])
        self.assertFalse(result["structural_checks"]["monthly_cadence_without_gaps"])
        self.assertFalse(result["structural_checks"]["audit_window_start_reached"])
        self.assertEqual(result["structural_eligibility"], "STRUCTURAL_ELIGIBILITY_NOT_ESTABLISHED")


    def test_parsed_output_is_reused_only_when_byte_identical(self):
        from pathlib import Path
        import tempfile
        rows = [{"date": "1913-01-01", "value": "9.8"}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "parsed.csv"
            first_hash = write_parsed(path, rows)
            original = path.read_bytes()
            self.assertEqual(write_parsed(path, rows), first_hash)
            self.assertEqual(path.read_bytes(), original)
            with self.assertRaises(RuntimeError):
                write_parsed(path, [{"date": "1913-01-01", "value": "9.9"}])
            self.assertEqual(path.read_bytes(), original)

    def test_source_contains_no_endpoint_estimator_imports(self):
        from pathlib import Path
        source = Path("analysis/prospective_raw_audit.py").read_text(encoding="utf-8")
        forbidden = ("canonical_primary_alpha", "generate_report", "statsmodels", "scipy.signal", "numpy.fft", "p_value")
        for token in forbidden:
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
