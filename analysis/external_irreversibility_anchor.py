import json
import hashlib
import time
import requests

REPORT_PATH = "artifacts/canonical_report.json"

ANCHOR_LOG = "data/external_anchor_log.json"

def load_report():
    with open(REPORT_PATH) as f:
        return json.load(f)

def compute_fingerprint(report):
    raw = json.dumps(report, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

def append_local_anchor(fingerprint):
    entry = {
        "timestamp": time.time(),
        "fingerprint": fingerprint
    }

    try:
        with open(ANCHOR_LOG) as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(ANCHOR_LOG, "w") as f:
        json.dump(data, f, indent=2)

def push_public_anchor(fingerprint):
    try:
        # مثال: إرسال hash إلى خدمة خارجية (placeholder)
        requests.post("https://httpbin.org/post", json={
            "fingerprint": fingerprint,
            "source": "maximal-one"
        }, timeout=5)
    except Exception as e:
        print("External anchor failed:", e)

def main():
    report = load_report()
    fingerprint = compute_fingerprint(report)

    print("=== EXTERNAL IRREVERSIBILITY ===")
    print("Fingerprint:", fingerprint)

    append_local_anchor(fingerprint)
    push_public_anchor(fingerprint)

if __name__ == "__main__":
    main()
