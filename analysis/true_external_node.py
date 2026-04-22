import requests
import hashlib
import json
import time

REPO = "ahmedpearl/maximal-one"

def fetch_latest_report():
    url = f"https://raw.githubusercontent.com/{REPO}/main/public/repro_bundle/canonical_report.json"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text

def compute_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def main():
    print("=== TRUE EXTERNAL NODE ===")

    data = fetch_latest_report()
    h = compute_hash(data)

    print("External hash:", h)

    with open("external_result.json", "w") as f:
        json.dump({
            "timestamp": time.time(),
            "external_hash": h,
            "source": "independent_node"
        }, f, indent=2)

if __name__ == "__main__":
    main()
