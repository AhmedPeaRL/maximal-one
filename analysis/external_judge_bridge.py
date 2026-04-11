import json
import hashlib
import requests
import time

"""
External Irreducible Judge Layer

This module sends minimal, non-biased output
to an external endpoint that CANNOT be influenced
by the internal system.

Goal:
Break closed epistemic loop.
"""

JUDGE_ENDPOINT = "https://httpbin.org/post"  # placeholder (replace later)

def load_core_result():
    try:
        with open("artifacts/canonical_report.json") as f:
            return json.load(f)
    except:
        return None


def extract_minimal_signal(report):
    return {
        "alpha": report.get("spectral_profile", {}).get("estimated_alpha"),
        "sigma": report.get("spectral_profile", {}).get("bootstrap_std"),
        "timestamp": time.time()
    }


def build_judge_payload(signal):
    raw = json.dumps(signal, sort_keys=True)
    signature = hashlib.sha256(raw.encode()).hexdigest()

    return {
        "signal": signal,
        "signature": signature
    }


def send_to_external_judge(payload):
    try:
        res = requests.post(JUDGE_ENDPOINT, json=payload, timeout=5)
        return res.status_code, res.text
    except Exception as e:
        return 500, str(e)


def main():
    report = load_core_result()

    if not report:
        print("No report found")
        return

    signal = extract_minimal_signal(report)

    payload = build_judge_payload(signal)

    status, response = send_to_external_judge(payload)

    print("External Judge Status:", status)

    with open("artifacts/external_judge_log.json", "w") as f:
        json.dump({
            "status": status,
            "response": response,
            "payload": payload
        }, f, indent=2)


if __name__ == "__main__":
    main()
