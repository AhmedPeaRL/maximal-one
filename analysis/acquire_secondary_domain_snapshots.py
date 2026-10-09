from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path.cwd()
SNAPSHOT_DIR = ROOT / "real-data" / "source-snapshots"
MANIFEST_PATH = SNAPSHOT_DIR / "secondary_source_manifest_v1.json"

SOURCES = {
    "hadcet_monthly": {
        "url": "https://www.metoffice.gov.uk/hadobs/hadcet/data/meantemp_monthly_totals.txt",
        "snapshot": SNAPSHOT_DIR / "hadcet_meantemp_monthly_totals.txt",
        "parsed": ROOT / "real-data" / "hadcet_monthly.csv",
        "publisher": "UK Met Office Hadley Centre",
        "identifier": "HadCET monthly mean temperature",
        "units": "degrees Celsius",
        "cadence": "monthly",
    },
    "fred_indpro": {
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDPRO",
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


def fetch_or_reuse(name: str, spec: dict, manifest: dict) -> bytes:
    path = spec["snapshot"]
    key = name
    if path.exists():
        if key not in manifest.get("sources", {}):
            raise RuntimeError(
                f"Existing raw snapshot has no manifest entry: {path}. "
                "Do not invent its retrieval date. Archive it and retrieve a fresh snapshot, "
                "or manually reconstruct provenance from a trustworthy acquisition record."
            )
        data = path.read_bytes()
        expected = manifest["sources"][key].get("raw_sha256")
        actual = sha256_bytes(data)
        if expected != actual:
            raise RuntimeError(f"Raw snapshot checksum mismatch for {path}: {actual}")
        print(f"REUSE {path} sha256={actual}")
        return data

    request = Request(
        spec["url"],
        headers={"User-Agent": "maximal-one-reproducible-research/1.0"},
    )
    with urlopen(request, timeout=60) as response:
        data = response.read()
        status = getattr(response, "status", 200)
        if status != 200:
            raise RuntimeError(f"HTTP {status} downloading {spec['url']}")
    if not data:
        raise RuntimeError(f"Empty download from {spec['url']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    record = {
        "source_identifier": spec["identifier"],
        "source_url": spec["url"],
        "publisher": spec["publisher"],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_snapshot_path": str(path.relative_to(ROOT)),
        "raw_sha256": sha256_bytes(data),
        "raw_bytes": len(data),
        "status": "SNAPSHOT_PRESERVED_PENDING_AUDIT",
    }
    manifest.setdefault("sources", {})[name] = record
    print(f"DOWNLOADED {path} sha256={record['raw_sha256']}")
    return data


def parse_hadcet(data: bytes) -> list[dict]:
    text = data.decode("utf-8-sig", errors="strict")
    rows: list[dict] = []
    for line in text.splitlines():
        match = re.match(r"^\s*(\d{4})\s+(.+?)\s*$", line)
        if not match:
            continue
        year = int(match.group(1))
        tokens = match.group(2).split()
        # Official table has 12 monthly values followed by an annual value.
        if len(tokens) < 12:
            continue
        for month, token in enumerate(tokens[:12], start=1):
            try:
                value = float(token)
                if not (value == value and abs(value) != float("inf")):
                    value_text = ""
                else:
                    value_text = format(value, ".12g")
            except ValueError:
                value_text = ""
            rows.append({"date": f"{year:04d}-{month:02d}-01", "value": value_text})
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
        date = (row.get(date_key) or "").strip()
        value = (row.get(value_key) or "").strip()
        if not date:
            continue
        if value in {".", "NA", "N/A", ""}:
            value = ""
        else:
            try:
                number = float(value)
                if not (number == number and abs(number) != float("inf")):
                    value = ""
                else:
                    value = format(number, ".12g")
            except ValueError:
                value = ""
        rows.append({"date": date, "value": value})
    if not rows:
        raise RuntimeError("No rows parsed from FRED INDPRO raw snapshot")
    return rows


def write_csv(path: Path, rows: list[dict]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return sha256_bytes(path.read_bytes())


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
            "sources": {},
            "claim_authority": False,
            "promotion_authority": False,
        }

    parsers = {"hadcet_monthly": parse_hadcet, "fred_indpro": parse_fred_indpro}
    for name, spec in SOURCES.items():
        raw = fetch_or_reuse(name, spec, manifest)
        # Persist provenance immediately after acquisition so that a later
        # source/parse failure cannot leave an unmanifested raw snapshot.
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        rows = parsers[name](raw)
        parsed_sha = write_csv(spec["parsed"], rows)
        source_record = manifest["sources"][name]
        source_record.update({
            "parsed_path": str(spec["parsed"].relative_to(ROOT)),
            "parsed_sha256": parsed_sha,
            "parsed_rows_including_missing_values": len(rows),
            "first_date": rows[0]["date"],
            "last_date": rows[-1]["date"],
            "cadence": spec["cadence"],
            "units": spec["units"],
            "status": "SNAPSHOT_PRESERVED_PENDING_TIME_AND_PROVENANCE_AUDIT",
        })
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"PARSED {name}: rows={len(rows)} sha256={parsed_sha}")

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    print("IMPORTANT: acquisition is not eligibility, replication, or claim support.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ACQUISITION BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(1)
