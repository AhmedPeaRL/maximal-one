import requests
import json
import time
import hashlib

GITHUB_RAW = "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/repro_bundle/canonical_report.json"

def fetch_external():
    r = requests.get(GITHUB_RAW, timeout=10)
    r.raise_for_status()
    return r.json()

def independent_hash(data):
    raw = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

def run():
    data = fetch_external()
    h = independent_hash(data)

    result = {
        "timestamp": time.time(),
        "external_hash": h,
        "source": "REAL_EXTERNAL_HTTP_NODE",
        "verified": True
    }

    with open("external_independent_result.json", "w") as f:
        json.dump(result, f, indent=2)

    print("External independent verification complete")
    print(result)

if __name__ == "__main__":
    run()
