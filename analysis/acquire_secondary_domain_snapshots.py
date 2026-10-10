from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path.cwd()
SNAPSHOT_DIR = ROOT / "real-data" / "source-snapshots"
MANIFEST_PATH = SNAPSHOT_DIR / "secondary_source_manifest_v1.json"
# Frozen before examining either candidate's alpha. Both domains end at the
# last complete calendar year available at protocol amendment time.
ANALYSIS_END = "2025-12-01"
MAX_ATTEMPTS_PER_URL = 2
TIMEOUT_SECONDS = 90

SOURCES = {
    "hadcet_monthly": {
        "urls": ["https://hadleyserver.metoffice.gov.uk/hadobs/hadcet/data/meantemp_monthly_totals.txt"],
        "snapshot": SNAPSHOT_DIR / "hadcet_meantemp_monthly_totals.txt",
        "parsed": ROOT / "real-data" / "hadcet_monthly.csv",
        "publisher": "UK Met Office Hadley Centre",
        "identifier": "HadCET monthly mean temperature",
        "units": "degrees Celsius",
        "cadence": "monthly",
    },
    "fred_indpro": {
        # First request only the frozen analysis window; retry the canonical
        # FRED endpoint if the bounded request fails. Record the exact URL used.
        "urls": [
            "https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDPRO&cosd=1919-01-01&coed=2025-12-01",
            "https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDPRO",
        ],
        "snapshot": SNAPSHOT_DIR / "fred_indpro.csv",
        "parsed": ROOT / "real-data" / "fred_indpro_monthly.csv",
        "publisher": "Board of Governors of the Federal Reserve System, distributed through FRED",
        "identifier": "FRED:INDPRO",
        "units": "index 2017=100, seasonally adjusted",
        "cadence": "monthly",
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(urls: list[str]) -> tuple[bytes, str]:
    errors: list[str] = []
    for url in urls:
        for attempt in range(1, MAX_ATTEMPTS_PER_URL + 1):
            try:
                request = Request(
                    url,
                    headers={
                        "User-Agent": "maximal-one-reproducible-research/1.2",
                        "Accept": "text/csv,text/plain,*/*",
                    },
                )
                with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                    status = getattr(response, "status", 200)
                    if status != 200:
                        raise RuntimeError(f"HTTP {status} downloading {url}")
                    data = response.read()
                if not data:
                    raise RuntimeError(f"Empty download from {url}")
                return data, url
            except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
                message = f"{type(exc).__name__}: {exc}"
                errors.append(f"{url} attempt {attempt}/{MAX_ATTEMPTS_PER_URL}: {message}")
                print(
                    f"DOWNLOAD_ATTEMPT_FAILED {attempt}/{MAX_ATTEMPTS_PER_URL}: {url}: {message}",
                    file=sys.stderr,
                    flush=True,
                )
                if attempt < MAX_ATTEMPTS_PER_URL:
                    time.sleep(min(2 ** attempt, 8))
    raise RuntimeError("all source URL attempts failed: " + " | ".join(errors))


def fetch_or_reuse(name: str, spec: dict, manifest: dict) -> bytes:
    path = spec["snapshot"]
    if path.exists():
        record = manifest.get("sources", {}).get(name)
        if not record:
            raise RuntimeError(f"Existing raw snapshot has no manifest entry: {path}; refusing to invent retrieval provenance")
        data = path.read_bytes()
        actual = sha256_bytes(data)
        if actual != record.get("raw_sha256"):
            raise RuntimeError(f"Raw snapshot checksum mismatch for {path}: {actual}")
        print(f"REUSE {path} sha256={actual}")
        return data

    data, used_url = fetch_bytes(spec["urls"])
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write only after a complete response has been read.
    path.write_bytes(data)
    manifest.setdefault("sources", {})[name] = {
        "source_identifier": spec["identifier"],
        "source_url": used_url,
        "source_url_candidates": spec["urls"],
        "publisher": spec["publisher"],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_snapshot_path": str(path.relative_to(ROOT)),
        "raw_sha256": sha256_bytes(data),
        "raw_bytes": len(data),
        "analysis_window_start": None,
        "analysis_window_end_inclusive": ANALYSIS_END,
        "status": "SNAPSHOT_PRESERVED_PENDING_AUDIT",
    }
    print(f"DOWNLOADED {path} sha256={manifest['sources'][name]['raw_sha256']}", flush=True)
    return data


def _value_text(token: str, *, hadcet: bool = False) -> str:
    token = token.strip()
    if not token:
        return ""
    try:
        value = float(token)
    except ValueError:
        return ""
    if not math.isfinite(value):
        return ""
    # Met Office's documented sentinel is missing data, not a temperature.
    if hadcet and math.isclose(value, -99.9, rel_tol=0.0, abs_tol=1e-9):
        return ""
    return format(value, ".12g")


def parse_hadcet(data: bytes) -> list[dict]:
    text = data.decode("utf-8-sig", errors="strict")
    rows: list[dict] = []
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
            if date_text > ANALYSIS_END:
                continue
            rows.append({"date": date_text, "value": _value_text(token, hadcet=True)})
    if not rows:
        raise RuntimeError("No monthly rows parsed from HadCET raw snapshot")
    return rows


def parse_fred_indpro(data: bytes) -> list[dict]:
    text = data.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise RuntimeError("FRED snapshot has no CSV header")
    fields = {field.strip().lower(): field for field in reader.fieldnames}
    date_key = fields.get("observation_date") or fields.get("date")
    value_key = fields.get("indpro") or fields.get("value")
    if not date_key or not value_key:
        raise RuntimeError(f"Unexpected FRED columns: {reader.fieldnames}")
    rows = []
    for row in reader:
        date_text = (row.get(date_key) or "").strip()
        if not date_text or date_text[:10] > ANALYSIS_END:
            continue
        value_text = _value_text((row.get(value_key) or "").strip())
        rows.append({"date": date_text[:10], "value": value_text})
    if not rows:
        raise RuntimeError("No monthly rows parsed from FRED INDPRO raw snapshot")
    return rows


def write_csv(path: Path, rows: list[dict]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return sha256_bytes(path.read_bytes())


def save_manifest(manifest: dict) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if manifest.get("protocol") != "SECONDARY_SOURCE_MANIFEST_V1":
            raise RuntimeError("Unexpected source manifest protocol")
    else:
        manifest = {
            "protocol": "SECONDARY_SOURCE_MANIFEST_V1",
            "status": "ACQUISITION_ONLY_NOT_REPLICATION_APPROVAL",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "analysis_window_end_inclusive": ANALYSIS_END,
            "window_policy": "Fixed cutoff at last complete calendar year before candidate endpoint analysis; no alpha-based cutoff selection.",
            "sources": {}, "errors": [], "claim_authority": False, "promotion_authority": False,
        }
    manifest["analysis_window_end_inclusive"] = ANALYSIS_END
    manifest.setdefault("errors", [])
    manifest["errors"] = []
    parsers = {"hadcet_monthly": parse_hadcet, "fred_indpro": parse_fred_indpro}
    for name, spec in SOURCES.items():
        try:
            raw = fetch_or_reuse(name, spec, manifest)
            save_manifest(manifest)
            rows = parsers[name](raw)
            parsed_sha = write_csv(spec["parsed"], rows)
            record = manifest["sources"][name]
            record.update({
                "parsed_path": str(spec["parsed"].relative_to(ROOT)),
                "parsed_sha256": parsed_sha,
                "parsed_rows_including_missing_values": len(rows),
                "missing_value_rows": sum(not row["value"] for row in rows),
                "first_date": rows[0]["date"], "last_date": rows[-1]["date"],
                "analysis_window_end_inclusive": ANALYSIS_END,
                "cadence": spec["cadence"], "units": spec["units"],
                "status": "SNAPSHOT_PRESERVED_PENDING_TIME_AND_PROVENANCE_AUDIT",
            })
            save_manifest(manifest)
            print(f"PARSED {name}: rows={len(rows)} missing={record['missing_value_rows']} last={record['last_date']} sha256={parsed_sha}", flush=True)
        except Exception as exc:
            message = f"{name}: {type(exc).__name__}: {exc}"
            manifest["errors"].append(message)
            source_record = manifest.setdefault("sources", {}).get(name)
            if source_record is not None:
                source_record["status"] = "ACQUISITION_OR_PARSE_FAILED_PENDING_REVIEW"
                source_record["last_error"] = message
            save_manifest(manifest)
            print(f"SOURCE_FAILED {message}", file=sys.stderr, flush=True)
            # Continue to the other source so one timeout does not erase useful evidence.
    manifest["status"] = "ACQUISITION_COMPLETE_PENDING_AUDIT" if not manifest["errors"] else "PARTIAL_ACQUISITION_BLOCKED"
    save_manifest(manifest)
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}", flush=True)
    print("Acquisition is not eligibility, independence, replication, or claim support.", flush=True)
    return 0 if not manifest["errors"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ACQUISITION BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(1)
