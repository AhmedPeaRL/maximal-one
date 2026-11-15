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
        headers={"User-Agent": "HCM-WDC-SILSO-Provenance-Audit/1.0"}
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        data = response.read()

    if not data:
        raise RuntimeError(f"Empty download: {url}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return data


def read_semicolon_rows(path: Path) -> list[list[str]]:
    text = path.read_text(encoding="utf-8-sig")
    rows = []

    for row in csv.reader(io.StringIO(text), delimiter=";"):
        if not row:
            continue

        row = [field.strip() for field in row]

        if len(row) != 7:
            raise ValueError(
                f"{path}: expected 7 fields, found {len(row)}: {row}"
            )

        if not row[0].isdigit() or not row[1].isdigit():
            raise ValueError(f"Unexpected non-data row: {row}")

        rows.append(row)

    return rows


def month_key(row: list[str]) -> tuple[int, int]:
    year = int(row[0])
    month = int(row[1])

    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {row}")

    return year, month


def check_month_sequence(rows: list[list[str]]) -> dict:
    keys = [month_key(row) for row in rows]

    duplicates = len(keys) - len(set(keys))
    gaps = []

    for previous, current in zip(keys, keys[1:]):
        y, m = previous
        m += 1
        if m == 13:
            y += 1
            m = 1

        if current != (y, m):
            gaps.append({
                "previous": list(previous),
                "next": list(current)
            })

    return {
        "rows": len(rows),
        "duplicate_months": duplicates,
        "gap_count": len(gaps),
        "first_month": list(keys[0]) if keys else None,
        "last_month": list(keys[-1]) if keys else None,
        "gaps_sample": gaps[:20]
    }


def main() -> int:
    if not CURRENT.exists():
        raise FileNotFoundError(CURRENT)

    OUT.mkdir(parents=True, exist_ok=True)

    csv_path = OUT / "SN_m_tot_V2.0.csv"
    txt_path = OUT / "SN_m_tot_V2.0.txt"

    csv_bytes = download(CSV_URL, csv_path)
    txt_bytes = download(TXT_URL, txt_path)

    current_bytes = CURRENT.read_bytes()

    official_rows = read_semicolon_rows(csv_path)
    current_rows = read_semicolon_rows(CURRENT)

    official_by_month = {
        month_key(row): row for row in official_rows
    }

    first_mismatch = None
    compared = 0

    for index, current_row in enumerate(current_rows):
        key = month_key(current_row)
        official_row = official_by_month.get(key)

        if official_row is None:
            first_mismatch = {
                "row_index": index,
                "month": list(key),
                "reason": "MONTH_MISSING_FROM_OFFICIAL_SOURCE"
            }
            break

        compared += 1

        if current_row != official_row:
            first_mismatch = {
                "row_index": index,
                "month": list(key),
                "current_row": current_row,
                "official_row": official_row
            }
            break

    current_sequence = check_month_sequence(current_rows)
    official_sequence = check_month_sequence(official_rows)

    official_last = month_key(official_rows[-1])
    current_last = month_key(current_rows[-1])

    newer_rows = [
        row for row in official_rows
        if month_key(row) > current_last
    ]

    prefix_match = (
        first_mismatch is None
        and compared == len(current_rows)
        and len(official_rows) >= len(current_rows)
    )

    if not prefix_match:
        status = "MISMATCH_REQUIRES_MANUAL_REVIEW"
    elif len(official_rows) == len(current_rows):
        status = "EXACT_WINDOW_MATCH"
    else:
        status = "PREFIX_MATCH_WITH_NEWER_OFFICIAL_TAIL"

    try:
        git_blob = subprocess.check_output(
            ["git", "hash-object", str(CURRENT)],
            cwd=ROOT,
            text=True
        ).strip()
    except Exception:
        git_blob = None

    report = {
        "schema": "HCM_WDC_SILSO_SOURCE_COMPARISON_V1",
        "status": status,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "identifier": "WDC-SILSO SN_m_tot_V2.0 monthly total sunspot number",
            "doi": DOI,
            "license": LICENSE,
            "csv_url": CSV_URL,
            "txt_url": TXT_URL
        },
        "current_analysis_file": {
            "path": str(CURRENT.relative_to(ROOT)),
            "sha256": sha256(current_bytes),
            "git_blob_sha1": git_blob,
            "sequence": current_sequence
        },
        "official_csv_snapshot": {
            "path": str(csv_path.relative_to(ROOT)),
            "sha256": sha256(csv_bytes),
            "bytes": len(csv_bytes),
            "sequence": official_sequence
        },
        "official_txt_snapshot": {
            "path": str(txt_path.relative_to(ROOT)),
            "sha256": sha256(txt_bytes),
            "bytes": len(txt_bytes)
        },
        "comparison": {
            "compared_rows": compared,
            "prefix_match": prefix_match,
            "first_mismatch": first_mismatch,
            "newer_official_rows_not_appended": len(newer_rows),
            "newer_official_tail_first_month": (
                list(month_key(newer_rows[0])) if newer_rows else None
            ),
            "newer_official_tail_last_month": (
                list(month_key(newer_rows[-1])) if newer_rows else None
            ),
            "analysis_file_modified": False
        },
        "replication_eligible": False,
        "interpretation": (
            "This is the primary solar dataset. Provenance reconciliation "
            "does not grant secondary replication eligibility."
        )
    }

    report_path = OUT / "comparison_report.json"
    report_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8"
    )

    print(json.dumps(report, indent=2))

    return 0 if prefix_match else 1


if __name__ == "__main__":
    sys.exit(main())
