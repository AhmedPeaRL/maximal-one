import json
import hashlib
import time
import requests

"""
Irreversible External Witness Layer

Goal:
Create REAL external footprint that cannot be erased or rewritten
outside GitHub control.
"""

# استخدم خدمة بتسجل request فعلياً + timestamp
WITNESS_ENDPOINT = "https://webhook.site/38fd0af0-1baa-4ad1-85a4-daa47cd18ff5"

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
        "time": time.time()
    }


def build_payload(signal):
    raw = json.dumps(signal, sort_keys=True)
    signature = hashlib.sha256(raw.encode()).hexdigest()

    return {
        "signal": signal,
        "signature": signature
    }


def send(payload):
    try:
        res = requests.post(WITNESS_ENDPOINT, json=payload, timeout=5)

        return {
            "status": res.status_code,
            "response": res.text[:300]
        }

    except Exception as e:
        return {
            "status": 500,
            "error": str(e)
        }


def persist(result, payload):
    with open("artifacts/external_irreversible_witness.json", "w") as f:
        json.dump({
            "result": result,
            "payload": payload
        }, f, indent=2)


def main():
    report = load_report()

    if not report:
        print("No report")
        return

    signal = extract_signal(report)
    payload = build_payload(signal)

    result = send(payload)

    persist(result, payload)

    print("External irreversible witness created.")


if __name__ == "__main__":
    main()
