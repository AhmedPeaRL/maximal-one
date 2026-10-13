import hashlib
import json
import os
import time
from datetime import datetime, timezone

import requests

GITHUB_RAW = (
    "https://raw.githubusercontent.com/"
    "AhmedPeaRL/maximal-one/main/artifacts/canonical_report.json"
)

LOCAL_REPORT = "artifacts/canonical_report.json"
AUDIT_REPORT = "artifacts/public_artifact_consistency_audit.json"

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def canonicalize_json(raw_text):
    parsed = json.loads(raw_text)
    return json.dumps(
        parsed,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )

def read_local_report():
    with open(LOCAL_REPORT, "r", encoding="utf-8") as handle:
        raw = handle.read()
    normalized = canonicalize_json(raw)
    return normalized, sha256_text(normalized)

def fetch_public_report(attempts=4, delay_seconds=5):
    last_error = None
    session = requests.Session()

    for attempt in range(1, attempts + 1):
        try:
            response = session.get(
                GITHUB_RAW,
                params={"audit_attempt": attempt, "ts": time.time_ns()},
                headers={
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "Accept": "application/json",
                },
                timeout=20,
            )
            response.raise_for_status()

            normalized = canonicalize_json(response.text)
            return normalized, sha256_text(normalized), None

        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            print(
                f"Public artifact fetch attempt "
                f"{attempt}/{attempts} failed: {last_error}"
            )

            if attempt < attempts:
                time.sleep(delay_seconds)

    return None, None, last_error

def write_audit(payload):
    os.makedirs(os.path.dirname(AUDIT_REPORT), exist_ok=True)
    with open(AUDIT_REPORT, "w", encoding="utf-8") as handle:
        json.dump(
            payload,
            handle,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        handle.write("\n")

def main():
    audit = {
        "schema": "PUBLIC_ARTIFACT_CONSISTENCY_AUDIT_V1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Compare the local canonical report with the currently "
            "published public report. This is not independent "
            "scientific reproduction."
        ),
        "independent_scientific_reproduction": False,
        "claim_support": False,
        "promotion_authority": False,
    }

    try:
        local_normalized, local_hash = read_local_report()
        audit["local_report_sha256"] = local_hash
    except Exception as exc:
        audit["status"] = "LOCAL_REPORT_INVALID"
        audit["error"] = f"{type(exc).__name__}: {exc}"
        write_audit(audit)
        print(json.dumps(audit, indent=2))
        raise SystemExit(1)

    public_normalized, public_hash, fetch_error = fetch_public_report()

    if public_normalized is None:
        audit["status"] = "UNAVAILABLE"
        audit["public_fetch_error"] = fetch_error
        audit["interpretation"] = (
            "The public artifact could not be retrieved reliably. "
            "No match or mismatch conclusion can be drawn."
        )
    else:
        audit["public_report_sha256"] = public_hash

        if local_hash == public_hash:
            audit["status"] = "MATCH"
            audit["interpretation"] = (
                "The local and currently published JSON reports match "
                "after JSON key-order canonicalization only."
            )
        else:
            audit["status"] = "MISMATCH"
            audit["interpretation"] = (
                "The local and currently published reports differ. "
                "They may originate from different workflow runs. "
                "Inspect commit identity and publication order before "
                "drawing conclusions."
            )

    write_audit(audit)
    print(json.dumps(audit, indent=2))

    # This is an explicitly diagnostic audit, not a scientific gate.
    # MATCH does not establish independent reproduction.
    # MISMATCH or UNAVAILABLE must remain visible for review.
    return 0

if __name__ == "__main__":
    main()
