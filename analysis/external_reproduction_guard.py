import os
import json
import time
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
        report,
        sort_keys=True,
        separators=(",", ":")
    ).encode()

    return hashlib.sha256(blob).hexdigest()

def fetch_external_fingerprint(url, retries=10, delay=15):
    if not url:
        print("⚠️ External URL not set")
        return None

    last = None

    for i in range(retries):
        try:
            print(f"Attempt {i+1}/{retries}")

            r = requests.get(
                url,
                timeout=20,
                headers={
                    "Cache-Control": "no-cache"
                }
            )

            r.raise_for_status()

            value = r.text.strip()

            if value:
                print("Fetched external fingerprint:", value)
                return value

            last = value

        except Exception as e:
            print("Fetch failed:", str(e))
            last = str(e)

        time.sleep(delay)

    raise RuntimeError(
        f"Unable to fetch stable external fingerprint: {last}"
    )

def validate(local_fp, external_fp):
    print("Local FP:", local_fp)
    print("External FP:", external_fp)

    if external_fp is None:
        raise SystemExit("❌ Missing external fingerprint")

    if local_fp != external_fp:
        raise SystemExit("❌ External reproduction mismatch")

    print("✅ External reproduction MATCH")

if __name__ == "__main__":
    report = load_report()

    local_fp = compute_fingerprint(report)

    external_fp = fetch_external_fingerprint(
        EXTERNAL_SOURCE_URL
    )

    validate(local_fp, external_fp)
