import requests
import hashlib
import json
import time

PUBLIC_ENDPOINTS = [
    "https://httpbin.org/post",
    "https://postman-echo.com/post"
]

def load_bundle():
    with open("public/repro_bundle/canonical_report.json") as f:
        report = json.load(f)

    with open("public/repro_bundle/report.hash") as f:
        report_hash = f.read().strip()

    return report, report_hash

def compute_hash(report):
    raw = json.dumps(report, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

def broadcast(report, report_hash):
    payload = {
        "timestamp": time.time(),
        "hash": report_hash,
        "system": "maximal-one"
    }

    results = []

    for url in PUBLIC_ENDPOINTS:
        try:
            r = requests.post(url, json=payload, timeout=10)
            results.append({
                "endpoint": url,
                "status": r.status_code
            })
        except Exception as e:
            results.append({
                "endpoint": url,
                "status": "failed",
                "error": str(e)
            })

    return results

def main():
    report, report_hash = load_bundle()

    local_hash = compute_hash(report)

    if local_hash != report_hash:
        print("❌ Local integrity mismatch")
        return

    print("✅ Local integrity verified")

    results = broadcast(report, report_hash)

    with open("public/external_witness_log.json","w") as f:
        json.dump(results, f, indent=2)

    print("🌍 External broadcast complete")

if __name__ == "__main__":
    main()
