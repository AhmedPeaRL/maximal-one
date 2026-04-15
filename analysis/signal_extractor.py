import json
import os
import time

OUTPUT_PATH = "public/extracted_signal.json"

def load_truth():
    try:
        with open("public/live_truth.json") as f:
            return json.load(f)
    except:
        return None

def load_report():
    try:
        with open("artifacts/canonical_report.json") as f:
            return json.load(f)
    except:
        return None

def extract_signal(truth, report):
    if not truth or not report:
        return {
            "status": "no_data",
            "timestamp": time.time()
        }

    signal = {
        "timestamp": time.time(),
        "decision": truth.get("decision", {}).get("global"),
        "confidence": truth.get("scientific_signal", {}).get("confidence"),
        "alpha": truth.get("scientific_signal", {}).get("alpha"),
        "sigma": truth.get("scientific_signal", {}).get("sigma"),
        "verdict": "actionable" if truth.get("scientific_signal", {}).get("confidence", 0) > 0.9 else "weak",
        "market_hint": build_market_hint(truth)
    }

    return signal

def build_market_hint(truth):
    confidence = truth.get("scientific_signal", {}).get("confidence", 0)

    if confidence > 0.95:
        return "high-confidence anomaly detection"
    elif confidence > 0.9:
        return "predictive signal candidate"
    else:
        return "exploratory pattern"

def persist(signal):
    os.makedirs("public", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(signal, f, indent=2)

if __name__ == "__main__":
    truth = load_truth()
    report = load_report()

    signal = extract_signal(truth, report)
    persist(signal)

    print("Signal extracted:", signal)
