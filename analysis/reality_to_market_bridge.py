import json
import time
import os

OUTPUT_PATH = "data/market_signal.json"

THRESHOLD_CONFIDENCE = 0.75
THRESHOLD_ALPHA_SHIFT = 0.02

def load_signal():
    try:
        with open("artifacts/canonical_report.json") as f:
            r = json.load(f)

        alpha = r["spectral_profile"]["estimated_alpha"]
        sigma = r["spectral_profile"]["bootstrap_std"]

        return {
            "alpha": alpha,
            "sigma": sigma,
            "confidence": max(0.0, min(1.0, 1 - sigma))
        }
    except Exception:
        return None

def load_previous():
    if not os.path.exists(OUTPUT_PATH):
        return None
    with open(OUTPUT_PATH) as f:
        return json.load(f)

def decide(signal, prev):
    if signal is None:
        return {"action": "hold", "reason": "no_signal"}

    if signal["confidence"] < THRESHOLD_CONFIDENCE:
        return {"action": "hold", "reason": "low_confidence"}

    if prev is None:
        return {"action": "observe", "reason": "first_signal"}

    delta_alpha = abs(signal["alpha"] - prev["alpha"])

    if delta_alpha > THRESHOLD_ALPHA_SHIFT:
        return {
            "action": "micro_trade",
            "direction": "buy" if signal["alpha"] > prev["alpha"] else "sell",
            "strength": min(1.0, delta_alpha * 10)
        }

    return {"action": "hold", "reason": "stable_field"}

def main():
    signal = load_signal()
    prev = load_previous()

    decision = decide(signal, prev)

    payload = {
        "timestamp": time.time(),
        "signal": signal,
        "decision": decision
    }

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print("Market signal generated:", decision)

if __name__ == "__main__":
    main()
