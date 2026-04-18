import json
import os
import time

REPORT_PATH = "artifacts/canonical_report.json"
OUTPUT_PATH = "public/market_decision.json"

def load_signal():
    try:
        with open(REPORT_PATH) as f:
            r = json.load(f)

        alpha = r["spectral_profile"]["estimated_alpha"]
        sigma = r["spectral_profile"]["bootstrap_std"]

        confidence = max(0.0, min(1.0, 1 - sigma))

        return alpha, sigma, confidence

    except Exception:
        return None, None, 0.0


def decide(alpha, sigma, confidence):
    if alpha is None:
        return "NO_SIGNAL", "missing data"

    if confidence > 0.8 and 0.5 < alpha < 2.0:
        return "SELL", "strong invariant detected"

    if confidence > 0.6:
        return "HOLD", "signal present but not strong"

    return "KILL", "weak or unstable signal"


def main():
    alpha, sigma, confidence = load_signal()

    decision, reason = decide(alpha, sigma, confidence)

    result = {
        "timestamp": time.time(),
        "alpha": alpha,
        "sigma": sigma,
        "confidence": confidence,
        "decision": decision,
        "reason": reason
    }

    os.makedirs("public", exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print("Market decision generated:", decision)


if __name__ == "__main__":
    main()
