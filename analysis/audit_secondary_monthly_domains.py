from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import date
from pathlib import Path

ROOT = Path.cwd()
MANIFEST_PATH = ROOT / "real-data/source-snapshots/secondary_source_manifest_v1.json"
OUTPUT_PATH = ROOT / "artifacts/secondary_data_integrity_audit.json"
MIN_ROWS = 1024
ANALYSIS_END = "2025-12-01"
DATASETS = {
    "hadcet_monthly": ROOT / "real-data/hadcet_monthly.csv",
    "fred_indpro": ROOT / "real-data/fred_indpro_monthly.csv",
}


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def month_index(value: str) -> int:
    parsed = date.fromisoformat(value)
    if parsed.day != 1:
        raise ValueError(f"date is not first day of month: {value}")
    return parsed.year * 12 + parsed.month - 1


def audit_one(name: str, path: Path, manifest: dict) -> dict:
    reasons: list[str] = []
    record = manifest.get("sources", {}).get(name, {})
    raw_rel = record.get("raw_snapshot_path")
    raw_path = ROOT / raw_rel if raw_rel else ROOT / "__missing_raw_snapshot__"
    rows: list[tuple[str, int, float | None]] = []
    if not record:
        reasons.append("source_manifest_entry_missing")
    if not path.is_file():
        reasons.append("parsed_file_missing")
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != ["date", "value"]:
                reasons.append("unexpected_columns_expected_date_value")
            for line_no, row in enumerate(reader, start=2):
                date_text = (row.get("date") or "").strip()
                value_text = (row.get("value") or "").strip()
                try:
                    index = month_index(date_text)
                except Exception:
                    reasons.append(f"invalid_month_date_at_line_{line_no}")
                    continue
                value: float | None
                try:
                    value = float(value_text)
                    if not math.isfinite(value):
                        raise ValueError("nonfinite")
                except Exception:
                    reasons.append(f"missing_or_nonfinite_value_at_line_{line_no}")
                    value = None
                if date_text > ANALYSIS_END:
                    reasons.append(f"date_after_frozen_analysis_window_at_line_{line_no}")
                if value is not None:
                    if name == "hadcet_monthly" and not (-20.0 <= value <= 40.0):
                        reasons.append(f"hadcet_value_outside_plausibility_bounds_at_line_{line_no}")
                    if name == "fred_indpro" and not (0.0 < value <= 1000.0):
                        reasons.append(f"indpro_value_outside_plausibility_bounds_at_line_{line_no}")
                rows.append((date_text, index, value))

    indices = [row[1] for row in rows]
    if not rows:
        reasons.append("no_valid_rows")
    if len(rows) < MIN_ROWS:
        reasons.append("fewer_than_1024_monthly_observations")
    if indices != sorted(indices):
        reasons.append("dates_not_sorted")
    if len(set(indices)) != len(indices):
        reasons.append("duplicate_months")
    if len(indices) > 1 and any(b - a != 1 for a, b in zip(indices, indices[1:])):
        reasons.append("monthly_gaps_or_nonmonthly_steps")
    if rows and rows[-1][0] != ANALYSIS_END:
        reasons.append("last_date_does_not_match_frozen_analysis_window_end_2025_12")

    raw_sha = sha256_file(raw_path)
    parsed_sha = sha256_file(path)
    if raw_sha is None:
        reasons.append("raw_snapshot_missing")
    elif raw_sha != record.get("raw_sha256"):
        reasons.append("raw_snapshot_checksum_mismatch")
    if parsed_sha is None:
        reasons.append("parsed_file_missing")
    elif parsed_sha != record.get("parsed_sha256"):
        reasons.append("parsed_snapshot_checksum_mismatch")

    passed = not reasons
    numeric = [r[2] for r in rows if r[2] is not None]
    return {
        "name": name,
        "parsed_path": str(path.relative_to(ROOT)),
        "raw_snapshot_path": record.get("raw_snapshot_path"),
        "raw_sha256_actual": raw_sha,
        "parsed_sha256_actual": parsed_sha,
        "rows_including_missing": len(rows),
        "valid_numeric_rows": len(numeric),
        "missing_or_nonfinite_rows": len(rows) - len(numeric),
        "minimum_value": min(numeric) if numeric else None,
        "maximum_value": max(numeric) if numeric else None,
        "first_date": rows[0][0] if rows else None,
        "last_date": rows[-1][0] if rows else None,
        "analysis_window_end_inclusive": ANALYSIS_END,
        "expected_cadence": "monthly",
        "time_integrity_passed": passed,
        "replication_eligible": False,
        "provenance_approved": False,
        "status": "TIME_INTEGRITY_PASS_PENDING_INDEPENDENCE_AND_NULL_REVIEW" if passed else "BLOCKED",
        "failure_reasons": sorted(set(reasons)),
        "claim_support": False,
    }


def main() -> int:
    if MANIFEST_PATH.is_file():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            if manifest.get("protocol") != "SECONDARY_SOURCE_MANIFEST_V1":
                raise ValueError("Unexpected source manifest protocol")
        except Exception as exc:
            manifest = {}
            manifest_error = f"manifest_unreadable_or_invalid:{type(exc).__name__}:{exc}"
        else:
            manifest_error = None
    else:
        manifest = {}
        manifest_error = "acquisition_manifest_missing"

    results = {name: audit_one(name, path, manifest) for name, path in DATASETS.items()}
    if manifest_error:
        for item in results.values():
            item["time_integrity_passed"] = False
            item["status"] = "BLOCKED"
            item["failure_reasons"] = sorted(set(item["failure_reasons"] + [manifest_error]))
    manifest_errors = manifest.get("errors", []) if isinstance(manifest, dict) else []
    all_pass = all(x["time_integrity_passed"] for x in results.values()) and not manifest_errors
    output = {
        "protocol": "SECONDARY_MONTHLY_DATA_INTEGRITY_AUDIT_V1",
        "status": "TIME_INTEGRITY_PASS_PENDING_REVIEW" if all_pass else "BLOCKED",
        "analysis_window_end_inclusive": ANALYSIS_END,
        "manifest_errors": manifest_errors,
        "datasets": results,
        "claim_authority": False,
        "promotion_authority": False,
        "interpretation": "This audit checks raw/parsed identity, explicit monthly cutoff, gaps, missing values, and broad plausibility bounds. It does not approve provenance, independence, null adequacy, replication, or claim promotion.",
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
