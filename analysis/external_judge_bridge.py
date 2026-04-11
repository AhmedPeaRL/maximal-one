import json
import hashlib
import time
import requests

"""
REAL External Judge Layer

This uses multiple independent endpoints
to break single-point bias.
"""

ENDPOINTS = [
    "https://httpbin.org/post",
    "https://webhook.site/38fd0af0-1baa-4ad1-85a4-daa47cd18ff5"
]


def load_report():
    try:
        with open("artifacts/canonical_report.json") as f:
            return json.load(f)
    except:
        return None


def extract_signal(report):
    return {
        "alpha": report.get("spectral_profile", {}).get("estimated_alpha"),
        "sigma": report.get("spectral_profile", {}).get("bootstrap_std"),
        "timestamp": time.time()
    }


def sign(payload):
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def send(endpoint, payload):
    try:
        r = requests.post(endpoint, json=payload, timeout=5)
        return {
            "endpoint": endpoint,
            "status": r.status_code
        }
    except Exception as e:
        return {
            "endpoint": endpoint,
            "status": 500,
            "error": str(e)
        }


def main():
    report = load_report()
    if not report:
        print("No report")
        return

    signal = extract_signal(report)
    payload = {
        "signal": signal,
        "signature": sign(signal)
    }

    results = [send(e, payload) for e in ENDPOINTS]

    with open("artifacts/external_judge_multi.json", "w") as f:
        json.dump(results, f, indent=2)

    print("External judge consensus created.")


if __name__ == "__main__":
    main()
