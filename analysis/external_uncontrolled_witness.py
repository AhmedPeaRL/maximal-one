import requests
import hashlib
import json
import time

PUBLIC_ENDPOINT = "https://your-external-node.example/verify"

def load_bundle():
    with open("public/repro_bundle/canonical_report.json") as f:
        report = json.load(f)

    with open("public/repro_bundle/report.hash") as f:
        report_hash = f.read().strip()

    return report, report_hash

def compute_hash(report):
    raw = json.dumps(report, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

def send_to_external(report, report_hash):
    payload = {
        "timestamp": time.time(),
        "report": report,
        "hash": report_hash
    }

    try:
        r = requests.post(PUBLIC_ENDPOINT, json=payload, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

def main():
    report, report_hash = load_bundle()

    local_hash = compute_hash(report)

    if local_hash != report_hash:
        print("❌ Local integrity mismatch")
        return

    print("✅ Local integrity verified")

    status, response = send_to_external(report, report_hash)

    if status == 200:
        print("🌍 External witness accepted")
        print(response)
    else:
        print("⚠️ External witness unreachable or rejected")
        print(response)

if __name__ == "__main__":
    main()
