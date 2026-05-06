import json
import numpy as np
import hashlib
import requests

def load_report(path="artifacts/canonical_report.json"):
    with open(path, "r") as f:
        return json.load(f)

def compute_fingerprint(report):
    sp = report["spectral_profile"]

    alpha = round(float(sp["estimated_alpha"]), 6)
    sigma = round(float(sp["bootstrap_std"]), 6)

    vector = np.array([alpha, sigma], dtype=np.float64)
    return hashlib.sha256(vector.tobytes()).hexdigest()

def fetch_external_fingerprint(url):
    """
    لازم ده ييجي من مصدر خارجي حقيقي:
    - artifact upload
    - or GitHub release asset
    - or remote API
    """
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text.strip()

def validate(local_fp, external_fp):
    print("Local FP:", local_fp)
    print("External FP:", external_fp)

    if local_fp != external_fp:
        raise SystemExit("❌ External reproduction mismatch")

    print("✅ External reproduction MATCH")

if __name__ == "__main__":
    report = load_report()

    local_fp = compute_fingerprint(report)

    # لازم تستبدل ده برابط حقيقي
    EXTERNAL_SOURCE_URL = "https://your-external-artifact-url"

    external_fp = fetch_external_fingerprint(EXTERNAL_SOURCE_URL)

    validate(local_fp, external_fp)
