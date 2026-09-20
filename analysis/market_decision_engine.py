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

        return alpha, sigma

    except Exception:
        return None, None, 0.0

def decide(alpha, sigma):
    if alpha is None:
        return "NO_SIGNAL", "missing data"

    return (
        "OBSERVE",
        "Scientific report is diagnostic only; "
        "no market confidence is inferred from bootstrap sigma."
    )

def main():
    alpha, sigma = load_signal()

    decision, reason = decide(
        alpha,
        sigma,
    )

    result = {
        "timestamp": time.time(),
        "alpha": alpha,
        "sigma": sigma,
        "decision": decision,
        "reason": reason,
        "epistemic_policy": {
            "market_confidence_inferred_from_sigma": False,
            "scientific_report_is_not_a_trading_authorization": True,
        }
    }

    os.makedirs("public", exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print("Market decision generated:", decision)

if __name__ == "__main__":
    main()
