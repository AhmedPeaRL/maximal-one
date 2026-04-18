import json
import os

def load_signal():
    try:
        with open("public/extracted_signal.json") as f:
            return json.load(f)
    except:
        return {}

def score_market(signal):
    score = 0

    # وجود alpha واضح
    if signal.get("alpha") is not None:
        score += 1

    # ثقة عالية
    if signal.get("confidence", 0) > 0.7:
        score += 1

    # استقرار منخفض التشتت
    if signal.get("sigma", 1) < 0.3:
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

    result = {
        "score": score_market(signal),
    }

    result["classification"] = classify(result["score"])

    os.makedirs("public", exist_ok=True)

    with open("public/market_decision.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Market harness decision generated:", result)

if __name__ == "__main__":
    main()
