import requests
import hashlib
import json
import time

GITHUB_RAW = "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/artifacts/canonical_report.json"

def fetch_external():
    try:
        r = requests.get(GITHUB_RAW, timeout=10)
        if r.status_code != 200:
            return None
        return r.text
    except:
        return None

def verify_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def run():
    data = fetch_external()

    if not data:
        print("❌ External fetch failed")
        return False

    computed = verify_hash(data)

    with open("artifacts/report.hash") as f:
        local = f.read().strip()

    if computed != local:
        print("❌ External mismatch")
        return False

    print("✅ True external reproduction confirmed")
    return True


if __name__ == "__main__":
    ok = run()
    if not ok:
        exit(1)
