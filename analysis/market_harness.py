import json
import math
import os

SIGNAL_PATH = "public/extracted_signal.json"
OUTPUT_PATH = "public/market_decision.json"

def load_signal():
    try:
        with open(SIGNAL_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, TypeError):
        return {}

def finite_number(value):
    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)) and math.isfinite(value):
        return float(value)

    return None

def score_market(signal):
    """
    Exploratory market-facing diagnostic only.

    This function must never infer scientific truth, HCM causation,
    consciousness, mechanism, or claim support.

    Missing optional metrics are treated as unavailable, not as failures.
    """

    score = 0

    # Presence of a usable alpha value.
    alpha = finite_number(signal.get("alpha"))
    if alpha is not None:
        score += 1

    # Optional confidence diagnostic.
    confidence = finite_number(signal.get("confidence"))
    if confidence is not None and confidence > 0.7:
        score += 1

    # Optional uncertainty diagnostic.
    sigma = finite_number(signal.get("sigma"))
    if sigma is not None and sigma < 0.3:
        score += 1

    return score

def classify(score):
    if score == 3:
        return "high_value"
    elif score == 2:
        return "convertible"
    else:
        return "experimental"

def main():
    signal = load_signal()
    score = score_market(signal)

    result = {
        "score": score,
        "classification": classify(score),
        "role": "exploratory_market_diagnostic",
        "scientific_authority": False,
        "claim_support_authority": False,
        "hcm_causation_inferred": False,
        "missing_metrics_are_nonfatal": True,
    }

    os.makedirs("public", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    print("Market harness decision generated:", result)

if __name__ == "__main__":
    main()
