#!/usr/bin/env python3
"""Acquire and audit two prospective monthly sources without endpoint analysis.

This module deliberately imports only Python's standard library. It does not
import, invoke, or calculate any scientific endpoint, exponent, p-value, or
alpha statistic. Raw responses are written byte-for-byte and never overwritten.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
import platform
import re
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path.cwd()
RAW_DIR = ROOT / "real-data" / "prospective-raw-snapshots"
PARSED_DIR = ROOT / "real-data" / "prospective-parsed"
REPORT_PATH = ROOT / "artifacts" / "prospective_raw_audit_report.json"
MANIFEST_PATH = RAW_DIR / "prospective_raw_audit_manifest_v1.json"
# Frozen for this audit design before acquiring either source. This is an audit
# window only; it is not an approved confirmatory analysis window.
AUDIT_START = "1913-01-01"
AUDIT_END = "2025-12-01"
MIN_REPLICATION_OBSERVATIONS = 1024
ESTIMATOR_SEGMENT_LENGTH = 1024
MIN_FREQUENCY_BINS = 20
FREQUENCY_BAND = (0.01, 0.05)
TIMEOUT_SECONDS = 90

SOURCES = {
    "hadukp_ewp_monthly": {
        "url": "https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/monthly/HadEWP_monthly_totals.txt",
        "metadata_url": "https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/download.html",
        "filename": "hadukp_ewp_monthly_raw.txt",
        "parsed_filename": "hadukp_ewp_monthly_parsed.csv",
        "publisher": "UK Met Office Hadley Centre / National Climate Information Centre",
        "identifier": "HadUKP England and Wales monthly precipitation totals (EWP)",
        "units": "mm monthly total",
        "format": "year followed by 12 monthly values and an annual summary; annual summary is not parsed as a month",
        "sentinel_policy": "-99.9 is missing if encountered; never treated as a numeric observation",
    },
    "fred_cpiaucns_monthly": {
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS&cosd=1913-01-01&coed=2025-12-01",
        "metadata_url": "https://fred.stlouisfed.org/series/CPIAUCNS",
        "filename": "fred_cpiaucns_monthly_raw.csv",
        "parsed_filename": "fred_cpiaucns_monthly_parsed.csv",
        "publisher": "U.S. Bureau of Labor Statistics via FRED, Federal Reserve Bank of St. Louis",
        "identifier": "FRED series CPIAUCNS",
        "units": "Index 1982-1984=100, not seasonally adjusted",
        "format": "CSV with observation_date and CPIAUCNS columns",
        "sentinel_policy": "Blank or non-finite values are missing; no interpolation",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_source(url: str) -> tuple[bytes, dict[str, str | None]]:
    request = Request(url, headers={"User-Agent": "maximal-one-prospective-raw-audit/1.0", "Accept": "text/plain,text/csv,*/*"})
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        status = getattr(response, "status", 200)
        if status != 200:
            raise RuntimeError(f"HTTP status {status}")
        data = response.read()
        headers = response.headers
        metadata = {
            "http_status": str(status),
            "content_type": headers.get("Content-Type"),
            "content_length_header": headers.get("Content-Length"),
            "etag": headers.get("ETag"),
            "last_modified_header": headers.get("Last-Modified"),
            "server_date_header": headers.get("Date"),
        }
    if not data:
        raise RuntimeError("empty response body")
    return data, metadata


def parse_number(token: str, sentinel: str | None = None) -> str:
    token = token.strip()
    if not token:
        return ""
    try:
        value = float(token)
    except ValueError:
        return ""
    if not math.isfinite(value):
        return ""
    if sentinel is not None:
        try:
            if math.isclose(value, float(sentinel), rel_tol=0.0, abs_tol=1e-9):
                return ""
        except ValueError:
            pass
    return format(value, ".15g")


def parse_hadukp(raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8-sig", errors="strict")
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        match = re.match(r"^\s*(\d{4})\s+(.+?)\s*$", line)
        if not match:
            continue
        year = int(match.group(1))
        tokens = match.group(2).split()
        if len(tokens) < 12:
            continue
        for month, token in enumerate(tokens[:12], start=1):
            date_text = f"{year:04d}-{month:02d}-01"
            if AUDIT_START <= date_text <= AUDIT_END:
                rows.append({"date": date_text, "value": parse_number(token, sentinel="-99.9")})
    if not rows:
        raise RuntimeError("No monthly EWP rows parsed; raw file preserved, audit remains UNKNOWN")
    return rows


def parse_fred_cpiaucns(raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise RuntimeError("No CSV header found; raw file preserved, audit remains UNKNOWN")
    columns = {name.strip().lower(): name for name in reader.fieldnames if name}
    date_key = columns.get("observation_date") or columns.get("date")
    value_key = columns.get("cpiaucns") or columns.get("value")
    if not date_key or not value_key:
        raise RuntimeError(f"Unexpected CSV columns {reader.fieldnames!r}; raw file preserved")
    rows: list[dict[str, str]] = []
    for item in reader:
        date_text = (item.get(date_key) or "").strip()[:10]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_text):
            continue
        if AUDIT_START <= date_text <= AUDIT_END:
            rows.append({"date": date_text, "value": parse_number(item.get(value_key) or "")})
    if not rows:
        raise RuntimeError("No monthly CPIAUCNS rows parsed; raw file preserved, audit remains UNKNOWN")
    return rows


def parsed_csv_bytes(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=["date", "value"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def write_parsed(path: Path, rows: list[dict[str, str]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    expected = parsed_csv_bytes(rows)
    # The parsed representation is a derived file. Never overwrite it. On a
    # rerun, reuse only byte-identical output; otherwise fail closed.
    if path.exists():
        existing = path.read_bytes()
        if existing != expected:
            raise RuntimeError("parsed output already exists and differs from current parser output; preserve both and review")
        return sha256_bytes(existing)
    with path.open("xb") as handle:
        handle.write(expected)
    return sha256_bytes(expected)


def month_index(date_text: str) -> int:
    if not re.fullmatch(r"\d{4}-\d{2}-01", date_text):
        raise ValueError("monthly timestamp must be YYYY-MM-01")
    year, month = int(date_text[:4]), int(date_text[5:7])
    if not 1 <= month <= 12:
        raise ValueError("invalid month")
    return year * 12 + month - 1


def structural_audit(rows: list[dict[str, str]]) -> dict:
    dates = [row["date"] for row in rows]
    indices: list[int] = []
    invalid_dates: list[str] = []
    for date_text in dates:
        try:
            indices.append(month_index(date_text))
        except ValueError:
            invalid_dates.append(date_text)
    duplicate_count = len(indices) - len(set(indices))
    out_of_order = any(b <= a for a, b in zip(indices, indices[1:]))
    gaps = sum(1 for a, b in zip(indices, indices[1:]) if b - a != 1)
    missing_values = sum(not row["value"] for row in rows)
    valid_values = len(rows) - missing_values
    # Structural frequency-bin count only; no spectrum or endpoint is computed.
    nperseg = ESTIMATOR_SEGMENT_LENGTH if len(rows) >= ESTIMATOR_SEGMENT_LENGTH else 0
    bins = sum(1 for k in range(1, nperseg // 2 + 1) if FREQUENCY_BAND[0] < (k / nperseg) < FREQUENCY_BAND[1]) if nperseg else 0
    checks = {
        "minimum_replication_observation_count": len(rows) >= MIN_REPLICATION_OBSERVATIONS,
        "all_values_present_and_finite": missing_values == 0,
        "monthly_timestamps_valid": not invalid_dates,
        "no_duplicate_or_nonincreasing_timestamps": duplicate_count == 0 and not out_of_order,
        "monthly_cadence_without_gaps": gaps == 0,
        "minimum_declared_frequency_bin_count": bins >= MIN_FREQUENCY_BINS,
        "audit_window_start_reached": bool(dates) and dates[0] == AUDIT_START,
        "audit_window_end_reached": bool(dates) and dates[-1] == AUDIT_END,
    }
    return {
        "row_count_in_predeclared_audit_window": len(rows),
        "valid_numeric_observation_count": valid_values,
        "missing_or_nonfinite_value_count": missing_values,
        "first_timestamp": dates[0] if dates else None,
        "last_timestamp": dates[-1] if dates else None,
        "invalid_timestamp_count": len(invalid_dates),
        "duplicate_month_count": duplicate_count,
        "out_of_order_or_nonincreasing": out_of_order,
        "gap_or_nonmonthly_step_count": gaps,
        "canonical_segment_length_for_structural_check": nperseg,
        "strictly_interior_frequency_bins_in_declared_band": bins,
        "structural_checks": checks,
        "structural_eligibility": "STRUCTURAL_CHECKS_PASS_PENDING_INDEPENDENCE_AND_NULL_REVIEW" if all(checks.values()) else "STRUCTURAL_ELIGIBILITY_NOT_ESTABLISHED",
    }


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {"schema": "PROSPECTIVE_RAW_AUDIT_MANIFEST_V1", "created_at_utc": utc_now(), "sources": {}}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def acquire_and_audit(name: str, spec: dict, manifest: dict) -> dict:
    raw_path = RAW_DIR / spec["filename"]
    parsed_path = PARSED_DIR / spec["parsed_filename"]
    record = {
        "candidate_id": name,
        "source": spec["publisher"],
        "series": spec["identifier"],
        "source_url": spec["url"],
        "metadata_url": spec["metadata_url"],
        "source_identity_status": "DOCUMENTED_METADATA_ONLY",
        "source_vintage_status": "PENDING_RESPONSE_METADATA_REVIEW",
        "retrieved_at_utc": None,
        "source_vintage": "UNKNOWN",
        "raw_path": str(raw_path.relative_to(ROOT)),
        "raw_file_sha256": None,
        "raw_bytes": None,
        "parsed_path": str(parsed_path.relative_to(ROOT)),
        "parsed_data_sha256": None,
        "audit_window_start": AUDIT_START,
        "audit_window_end_inclusive": AUDIT_END,
        "units": spec["units"],
        "sentinel_policy": spec["sentinel_policy"],
        "timestamp_audit_status": "PENDING",
        "cadence_and_gap_audit_status": "PENDING",
        "missingness_audit_status": "PENDING",
        "structural_eligibility": "NOT_ESTABLISHED",
        "independence_review": "PENDING",
        "shared_nuisance_review": "PENDING",
        "confirmatory_null_adequacy": "PENDING",
        "prior_endpoint_exposure": "NOT_VERIFIED_BY_GLOBAL_HISTORICAL_AUDIT",
        "replication_approval": "NOT_APPROVED",
        "claim_support": False,
        "promotion_authority": False,
        "endpoint_computation_authorized": False,
    }
    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        PARSED_DIR.mkdir(parents=True, exist_ok=True)
        if raw_path.exists():
            previous = manifest.get("sources", {}).get(name, {})
            actual = sha256_file(raw_path)
            if not previous or actual != previous.get("raw_file_sha256"):
                raise RuntimeError("raw file already exists without a matching manifest hash; refusing overwrite or inferred provenance")
            raw_bytes = raw_path.read_bytes()
            record.update(previous)
            record["raw_file_sha256"] = actual
            record["raw_bytes"] = len(raw_bytes)
            record["raw_path"] = str(raw_path.relative_to(ROOT))
            http_meta = previous.get("http_metadata", {})
        else:
            raw_bytes, http_meta = download_source(spec["url"])
            # O_EXCL semantics via mode x; never overwrite raw bytes.
            with raw_path.open("xb") as handle:
                handle.write(raw_bytes)
            record["retrieved_at_utc"] = utc_now()
            record["raw_file_sha256"] = sha256_bytes(raw_bytes)
            record["raw_bytes"] = len(raw_bytes)
            record["http_metadata"] = http_meta
            record["source_vintage"] = http_meta.get("etag") or http_meta.get("last_modified_header") or "UNKNOWN"
        parser = parse_hadukp if name == "hadukp_ewp_monthly" else parse_fred_cpiaucns
        rows = parser(raw_bytes)
        parsed_hash = write_parsed(parsed_path, rows)
        record["parsed_data_sha256"] = parsed_hash
        record["parsed_row_count"] = len(rows)
        record["structural_audit"] = structural_audit(rows)
        record["structural_eligibility"] = record["structural_audit"]["structural_eligibility"]
        checks = record["structural_audit"]["structural_checks"]
        record["timestamp_audit_status"] = "PASS" if checks["monthly_timestamps_valid"] and checks["no_duplicate_or_nonincreasing_timestamps"] else "FAIL"
        record["cadence_and_gap_audit_status"] = "PASS" if checks["monthly_cadence_without_gaps"] else "FAIL"
        record["missingness_audit_status"] = "PASS" if checks["all_values_present_and_finite"] else "FAIL"
        record["status"] = "STRUCTURAL_AUDIT_COMPLETE_PENDING_INDEPENDENCE_AND_NULL_REVIEW" if all(checks.values()) else "STRUCTURAL_AUDIT_BLOCKED"
    except Exception as exc:
        record["status"] = "RAW_AUDIT_INCOMPLETE"
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["timestamp_audit_status"] = "UNKNOWN"
        record["cadence_and_gap_audit_status"] = "UNKNOWN"
        record["missingness_audit_status"] = "UNKNOWN"
        record["structural_eligibility"] = "NOT_ESTABLISHED"
        record["independence_review"] = "PENDING"
        record["shared_nuisance_review"] = "PENDING"
        record["confirmatory_null_adequacy"] = "PENDING"
    manifest.setdefault("sources", {})[name] = record
    return record


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    results = [acquire_and_audit(name, spec, manifest) for name, spec in SOURCES.items()]
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_structural = all(x.get("status") == "STRUCTURAL_AUDIT_COMPLETE_PENDING_INDEPENDENCE_AND_NULL_REVIEW" for x in results)
    report = {
        "schema": "PROSPECTIVE_RAW_AUDIT_REPORT_V1",
        "created_at_utc": utc_now(),
        "code_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID", "UNKNOWN"),
        "python_version": platform.python_version(),
        "status": "STRUCTURAL_AUDIT_COMPLETE_PENDING_INDEPENDENCE_AND_NULL_REVIEW" if all_structural else "RAW_AUDIT_INCOMPLETE_OR_STRUCTURALLY_BLOCKED",
        "audit_only": True,
        "endpoint_computation_performed": False,
        "claim_support": False,
        "promotion_authority": False,
        "confirmatory_protocol_frozen": False,
        "approved_independent_secondary_domains": 0,
        "minimum_independent_secondary_domains": 2,
        "replication_status": "0/2",
        "audit_window": {"start_inclusive": AUDIT_START, "end_inclusive": AUDIT_END, "status": "PREDECLARED_AUDIT_WINDOW_NOT_CONFIRMATORY_AUTHORIZATION"},
        "candidates": results,
        "interpretation": "This report records source acquisition, raw/parsed hashes, timestamps, missingness, cadence, and structural eligibility only. Structural validity does not establish domain independence, null adequacy, replication, or claim support. Any unresolved provenance or exposure field remains UNKNOWN/PENDING.",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if all_structural else 1


if __name__ == "__main__":
    raise SystemExit(main())
