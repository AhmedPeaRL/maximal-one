from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path.cwd()
MANIFEST_PATH = ROOT / "real-data/source-snapshots/secondary_source_manifest_v1.json"
OUTPUT_PATH = ROOT / "artifacts/secondary_data_integrity_audit.json"
MIN_ROWS = 1024
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
    reasons = []
    record = manifest.get("sources", {}).get(name, {})
    raw_path = ROOT / record.get("raw_snapshot_path", "__missing_raw_snapshot__")
    rows = []
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
                try:
                    value = float(value_text)
                    if not (value == value and abs(value) != float("inf")):
                        raise ValueError("nonfinite")
                except Exception:
                    reasons.append(f"missing_or_nonfinite_value_at_line_{line_no}")
                    value = None
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
    return {
        "name": name,
        "parsed_path": str(path.relative_to(ROOT)),
        "raw_snapshot_path": record.get("raw_snapshot_path"),
        "raw_sha256_actual": raw_sha,
        "parsed_sha256_actual": parsed_sha,
        "rows": len(rows),
        "first_date": rows[0][0] if rows else None,
        "last_date": rows[-1][0] if rows else None,
        "expected_cadence": "monthly",
        "time_integrity_passed": passed,
        "replication_eligible": False,
        "provenance_approved": False,
        "status": "TIME_INTEGRITY_PASS_PENDING_INDEPENDENCE_AND_NULL_REVIEW" if passed else "BLOCKED",
        "failure_reasons": sorted(set(reasons)),
        "claim_support": False,
    }


def main() -> int:
    if not MANIFEST_PATH.is_file():
        raise SystemExit("Missing acquisition manifest; run acquisition first.")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("protocol") != "SECONDARY_SOURCE_MANIFEST_V1":
        raise SystemExit("Unexpected source manifest protocol")
    results = {name: audit_one(name, path, manifest) for name, path in DATASETS.items()}
    output = {
        "protocol": "SECONDARY_MONTHLY_DATA_INTEGRITY_AUDIT_V1",
        "status": "TIME_INTEGRITY_PASS_PENDING_REVIEW" if all(x["time_integrity_passed"] for x in results.values()) else "BLOCKED",
        "datasets": results,
        "claim_authority": False,
        "promotion_authority": False,
        "interpretation": "This audit checks snapshot identity and monthly timestamp/value integrity only. It does not approve provenance, independence, null adequacy, replication, or claim promotion.",
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["status"] != "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
