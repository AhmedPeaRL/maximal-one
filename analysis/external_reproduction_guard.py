import os
import json
import numpy as np
import hashlib
import requests

EXTERNAL_SOURCE_URL = os.getenv("EXTERNAL_SOURCE_URL", "").strip()

def load_report(path="artifacts/canonical_report.json"):
    with open(path, "r") as f:
        return json.load(f)

def compute_fingerprint(report):
    sp = report["spectral_profile"]

    payload = {
        "alpha": round(float(sp["estimated_alpha"]), 6),
        "sigma": round(float(sp["bootstrap_std"]), 6),
        "ci_low": round(float(sp["ci_low"]), 6),
        "ci_high": round(float(sp["ci_high"]), 6),
        "noise_alpha": round(float(sp["noise_alpha"]), 6)
    }

    blob = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    ).encode()

    fp = hashlib.sha256(blob).hexdigest()

    return fp

def fetch_external_fingerprint(url):
    if not url:
        print("⚠️ External URL not set → skipping external reproduction check")
        return None

    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text.strip()

def validate(local_fp, external_fp):
    if external_fp is None:
        print("✅ External check skipped (no source provided)")
        return

    print("Local FP:", local_fp)
    print("External FP:", external_fp)

    if local_fp != external_fp:
        raise SystemExit("❌ External reproduction mismatch")

    print("✅ External reproduction MATCH")

if __name__ == "__main__":
    report = load_report()

    local_fp = compute_fingerprint(report)

    external_fp = fetch_external_fingerprint(EXTERNAL_SOURCE_URL)

    validate(local_fp, external_fp)
