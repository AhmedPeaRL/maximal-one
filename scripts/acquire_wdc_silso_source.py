from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "real-data" / "sunspots_full.csv"
OUT = ROOT / "real-data" / "source-snapshots" / "wdc_silso"

CSV_URL = "https://www.sidc.be/SILSO/INFO/snmtotcsv.php"
TXT_URL = "https://www.sidc.be/SILSO/DATA/SN_m_tot_V2.0.txt"
DOI = "10.24414/qnza-ac80"
LICENSE = "CC BY-NC 4.0"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str, destination: Path) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "HCM-WDC-SILSO-Provenance-Audit/2.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
    if not data:
        raise RuntimeError(f"Empty download: {url}")
    # Reject obvious HTML error pages rather than treating them as source data.
    prefix = data[:512].lstrip().lower()
    if b"<html" in prefix or b"<!doctype html" in prefix:
        raise RuntimeError(f"HTML response received instead of source data: {url}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return data


def read_rows(path: Path) -> list[list[str]]:
    raw = path.read_text(encoding="utf-8-sig")
    rows: list[list[str]] = []
    for line_no, row in enumerate(csv.reader(io.StringIO(raw), delimiter=";"), 1):
        if not row or all(not x.strip() for x in row):
            continue
        fields = [x.strip() for x in row]
        if len(fields) != 7:
            raise ValueError(
                f"{path}:{line_no}: expected 7 semicolon-delimited fields, "
                f"found {len(fields)}: {fields}"
            )
        if not fields[0].isdigit() or not fields[1].isdigit():
            raise ValueError(f"{path}:{line_no}: unexpected non-data row: {fields}")
        year, month = int(fields[0]), int(fields[1])
        if not 1 <= month <= 12:
            raise ValueError(f"{path}:{line_no}: invalid month {month}")
        rows.append(fields)
    return rows


def key(row: list[str]) -> tuple[int, int]:
    return int(row[0]), int(row[1])


def sequence_audit(rows: list[list[str]]) -> dict:
    keys = [key(row) for row in rows]
    duplicates = []
    seen = set()
    for i, k in enumerate(keys):
        if k in seen:
            duplicates.append({"row_index": i, "month": list(k)})
        seen.add(k)

    gaps = []
    out_of_order = []
    for i, (a, b) in enumerate(zip(keys, keys[1:]), start=1):
        y, m = a
        m += 1
        if m == 13:
            y, m = y + 1, 1
        expected = (y, m)
        if b != expected:
            gaps.append({
                "after_row_index": i - 1,
                "previous": list(a),
                "next": list(b),
                "expected_next": list(expected),
            })
        if b <= a:
            out_of_order.append({
                "after_row_index": i - 1,
                "previous": list(a),
                "next": list(b),
            })
    return {
        "row_count": len(rows),
        "duplicate_month_count": len(duplicates),
        "duplicate_months": duplicates,
        "gap_count": len(gaps),
        "gaps": gaps,
        "out_of_order_count": len(out_of_order),
        "out_of_order": out_of_order,
        "first_month": list(keys[0]) if keys else None,
        "last_month": list(keys[-1]) if keys else None,
    }


def main() -> int:
    if not CURRENT.is_file():
        raise FileNotFoundError(CURRENT)

    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "SN_m_tot_V2.0.csv"
    txt_path = OUT / "SN_m_tot_V2.0.txt"

    csv_bytes = download(CSV_URL, csv_path)
    txt_bytes = download(TXT_URL, txt_path)

    current_bytes = CURRENT.read_bytes()
    current_rows = read_rows(CURRENT)
    official_rows = read_rows(csv_path)

    current_sequence = sequence_audit(current_rows)
    official_sequence = sequence_audit(official_rows)

    mismatches = []
    missing_official_months = []
    for index, current_row in enumerate(current_rows):
        if index >= len(official_rows):
            missing_official_months.append({
                "row_index": index,
                "month": list(key(current_row)),
                "reason": "OFFICIAL_SOURCE_SHORTER_THAN_CURRENT_FILE",
            })
            continue
        official_row = official_rows[index]
        if key(current_row) != key(official_row):
            mismatches.append({
                "row_index": index,
                "current_month": list(key(current_row)),
                "official_month": list(key(official_row)),
                "reason": "MONTH_KEY_OR_ORDER_MISMATCH",
                "current_row": current_row,
                "official_row": official_row,
            })
        elif current_row != official_row:
            mismatches.append({
                "row_index": index,
                "month": list(key(current_row)),
                "reason": "FIELD_VALUE_MISMATCH",
                "current_row": current_row,
                "official_row": official_row,
            })

    current_keys = [key(x) for x in current_rows]
    official_keys = [key(x) for x in official_rows]
    prefix_keys_match = (
        len(official_keys) >= len(current_keys)
        and official_keys[:len(current_keys)] == current_keys
    )
    sequence_checks_passed = all(
        audit["duplicate_month_count"] == 0
        and audit["gap_count"] == 0
        and audit["out_of_order_count"] == 0
        for audit in (current_sequence, official_sequence)
    )
    prefix_match = (
        prefix_keys_match
        and not mismatches
        and not missing_official_months
        and sequence_checks_passed
    )

    newer_tail = official_rows[len(current_rows):] if len(official_rows) > len(current_rows) else []
    if not prefix_match:
        status = "MISMATCH_OR_SEQUENCE_FAILURE_REQUIRES_MANUAL_REVIEW"
    elif newer_tail:
        status = "CURRENT_FILE_EXACT_OFFICIAL_PREFIX_WITH_NEWER_TAIL"
    else:
        status = "EXACT_WINDOW_MATCH"

    try:
        git_blob_sha1 = subprocess.check_output(
            ["git", "hash-object", str(CURRENT)],
            cwd=ROOT,
            text=True,
        ).strip()
    except Exception:
        git_blob_sha1 = None

    report = {
        "schema": "HCM_WDC_SILSO_SOURCE_COMPARISON_V2",
        "status": status,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "identifier": "WDC-SILSO SN_m_tot_V2.0 monthly total sunspot number",
            "doi": DOI,
            "license": LICENSE,
            "csv_url": CSV_URL,
            "txt_url": TXT_URL,
        },
        "current_analysis_file": {
            "path": str(CURRENT.relative_to(ROOT)),
            "sha256": sha256(current_bytes),
            "git_blob_sha1": git_blob_sha1,
            "sequence_audit": current_sequence,
        },
        "official_csv_snapshot": {
            "path": str(csv_path.relative_to(ROOT)),
            "sha256": sha256(csv_bytes),
            "bytes": len(csv_bytes),
            "sequence_audit": official_sequence,
        },
        "official_txt_snapshot": {
            "path": str(txt_path.relative_to(ROOT)),
            "sha256": sha256(txt_bytes),
            "bytes": len(txt_bytes),
        },
        "comparison": {
            "current_rows": len(current_rows),
            "official_rows": len(official_rows),
            "compared_rows": min(len(current_rows), len(official_rows)),
            "prefix_keys_match": prefix_keys_match,
            "prefix_match": prefix_match,
            "sequence_checks_passed": sequence_checks_passed,
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
            "missing_official_month_count": len(missing_official_months),
            "missing_official_months": missing_official_months,
            "newer_official_rows_not_appended": len(newer_tail),
            "newer_official_tail_first_month": list(key(newer_tail[0])) if newer_tail else None,
            "newer_official_tail_last_month": list(key(newer_tail[-1])) if newer_tail else None,
            "analysis_file_modified": False,
        },
        "replication_eligible": False,
        "interpretation": (
            "This is the primary solar dataset, not a secondary replication domain. "
            "Provenance reconciliation does not grant replication eligibility. "
            "No official newer rows are appended automatically."
        ),
    }

    report_path = OUT / "comparison_report.json"
    report_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))
    return 0 if prefix_match else 1


if __name__ == "__main__":
    sys.exit(main())
