from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


RAW_PATH = Path("real-data/cosmic_rays.csv")
CLEAN_PATH = Path("real-data/cosmic_rays_clean.csv")
OUTPUT_PATH = Path(
    "artifacts/cosmic_rays_time_integrity_audit.json"
)

EXPECTED_CADENCE_SECONDS = 3600
MIN_REPLICATION_ROWS = 1024


def fail(message: str) -> None:
    raise SystemExit(f"COSMIC-RAY TIME AUDIT: FAIL: {message}")


def read_raw() -> pd.DataFrame:
    if not RAW_PATH.is_file():
        fail(f"Raw timestamped file is missing: {RAW_PATH}")

    rows = []

    with RAW_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        reader = csv.DictReader(handle)

        if not reader.fieldnames:
            fail("Raw file has no CSV header.")

        fields = {
            str(name).strip().lower(): name
            for name in reader.fieldnames
        }

        time_key = fields.get("t") or fields.get("timestamp")
        value_key = fields.get("value")

        if time_key is None or value_key is None:
            fail(
                "Raw file must have timestamp and value columns."
            )

        for line_number, row in enumerate(reader, start=2):
            raw_time = str(row.get(time_key, "")).strip()
            raw_value = str(row.get(value_key, "")).strip()

            # Some exports leave a trailing semicolon after the time.
            raw_time = raw_time.rstrip(";").strip()

            if not raw_time or not raw_value:
                fail(
                    f"Blank timestamp/value at CSV line {line_number}."
                )

            try:
                timestamp = pd.to_datetime(
                    raw_time, errors="raise", utc=True
                )
                value = float(raw_value)
            except Exception as exc:
                fail(
                    f"Cannot parse line {line_number}: {exc}"
                )

            if not np.isfinite(value):
                fail(
                    f"Non-finite value at CSV line {line_number}."
                )

            rows.append({
                "timestamp": timestamp,
                "value": value,
            })

    if not rows:
        fail("Raw file contains no observations.")

    return pd.DataFrame(rows)


def read_clean_values() -> np.ndarray:
    if not CLEAN_PATH.is_file():
        fail(f"Pipeline input is missing: {CLEAN_PATH}")

    frame = pd.read_csv(CLEAN_PATH)

    if "value" not in frame.columns:
        fail("Clean file has no 'value' column.")

    values = pd.to_numeric(
        frame["value"], errors="coerce"
    ).to_numpy(dtype=float)

    if not np.isfinite(values).all():
        fail("Clean file contains missing or non-finite values.")

    return values


def main() -> int:
    raw = read_raw()
    clean_values = read_clean_values()

    timestamps = pd.DatetimeIndex(raw["timestamp"])
    values = raw["value"].to_numpy(dtype=float)

    timestamp_valid = not timestamps.hasnans
    strictly_increasing = bool(timestamps.is_monotonic_increasing)
    unique_timestamps = bool(not timestamps.has_duplicates)

    deltas = timestamps.to_series().diff().dropna()
    delta_seconds = (
        deltas.dt.total_seconds().to_numpy(dtype=float)
    )

    exact_cadence = bool(
        len(delta_seconds) > 0
        and np.all(delta_seconds == EXPECTED_CADENCE_SECONDS)
    )

    gap_count = int(
        np.sum(delta_seconds > EXPECTED_CADENCE_SECONDS)
    )
    non_hourly_delta_count = int(
        np.sum(delta_seconds != EXPECTED_CADENCE_SECONDS)
    )

    # Longest run of consecutive observations exactly one hour apart.
    longest_run = 1
    current_run = 1

    for delta in delta_seconds:
        if delta == EXPECTED_CADENCE_SECONDS:
            current_run += 1
        else:
            current_run = 1
        longest_run = max(longest_run, current_run)

    same_row_count = len(values) == len(clean_values)
    values_match = bool(
        same_row_count
        and np.allclose(
            values,
            clean_values,
            rtol=0.0,
            atol=1e-10,
        )
    )

    n = int(len(values))

    # This audit never approves replication. It only checks time integrity.
    replication_eligible = False
    failures = []

    if not timestamp_valid:
        failures.append("invalid_timestamps")
    if not strictly_increasing:
        failures.append("timestamps_not_strictly_increasing")
    if not unique_timestamps:
        failures.append("duplicate_timestamps")
    if not exact_cadence:
        failures.append("timestamps_not_continuously_hourly")
    if longest_run < MIN_REPLICATION_ROWS:
        failures.append("no_hourly_contiguous_run_of_1024")
    if not values_match:
        failures.append("raw_clean_values_or_row_order_mismatch")
    if n < MIN_REPLICATION_ROWS:
        failures.append("fewer_than_1024_observations")

    output = {
        "audit": "COSMIC_RAYS_TIME_INTEGRITY_V1",
        "scientific_role": "data_integrity_diagnostic_only",
        "raw_path": str(RAW_PATH),
        "pipeline_input_path": str(CLEAN_PATH),
        "observations": n,
        "timestamp_valid": timestamp_valid,
        "timestamps_strictly_increasing": strictly_increasing,
        "timestamps_unique": unique_timestamps,
        "first_timestamp_utc": str(timestamps[0]),
        "last_timestamp_utc": str(timestamps[-1]),
        "expected_cadence_seconds": EXPECTED_CADENCE_SECONDS,
        "exactly_hourly_contiguous": exact_cadence,
        "gap_count": gap_count,
        "non_hourly_interval_count": non_hourly_delta_count,
        "longest_hourly_contiguous_run": int(longest_run),
        "clean_value_count_matches_raw": same_row_count,
        "clean_values_match_raw_in_order": values_match,
        "replication_eligible": replication_eligible,
        "approved_for_replication": False,
        "claim_support": False,
        "failure_reasons": failures,
        "interpretation": (
            "Timestamp integrity only. This audit does not establish "
            "source provenance, nuisance independence, null adequacy, "
            "scientific replication, or claim promotion."
        ),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(json.dumps(output, indent=2, sort_keys=True))

    if failures:
        print(
            "COSMIC-RAY TIME AUDIT: BLOCKED; "
            "do not use this series as replication evidence."
        )
        return 1

    print(
        "COSMIC-RAY TIME AUDIT: TIME CHECKS PASS ONLY; "
        "provenance and scientific eligibility remain unapproved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
