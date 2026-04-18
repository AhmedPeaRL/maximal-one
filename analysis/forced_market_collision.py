import json
import requests
import time
import os

OUTPUT_FILE = "public/market_collision_signal.json"

def load_signal():
    try:
        with open("artifacts/canonical_report.json") as f:
            r = json.load(f)

        return {
            "alpha": r["spectral_profile"]["estimated_alpha"],
            "sigma": r["spectral_profile"]["bootstrap_std"],
            "confidence": max(0.0, min(1.0, 1 - r["spectral_profile"]["bootstrap_std"]))
        }
    except:
        return None

def build_market_signal(signal):
    if not signal:
        return {
            "status": "no_signal",
            "action": "hold"
        }

    if signal["confidence"] > 0.75:
        return {
            "status": "strong_signal",
            "action": "publish"
        }

    if signal["confidence"] > 0.6:
        return {
            "status": "weak_signal",
            "action": "probe"
        }

    return {
        "status": "unstable",
        "action": "hold"
    }

def external_ping(payload):
    try:
        # Example external endpoint (replace later with real)
        requests.post("https://httpbin.org/post", json=payload, timeout=5)
        return True
    except:
        return False

def main():
    os.makedirs("public", exist_ok=True)

    signal = load_signal()
    decision = build_market_signal(signal)

    payload = {
        "timestamp": time.time(),
        "decision": decision,
        "signal": signal
    }

    success = external_ping(payload)

    payload["external_contact"] = success

    with open(OUTPUT_FILE, "w") as f:
        json.dump(payload, f, indent=2)

    print("Forced market collision executed.")

if __name__ == "__main__":
    main()
