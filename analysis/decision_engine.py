import json
import os

REPORT_PATH = "artifacts/canonical_report.json"
OUTPUT_PATH = "artifacts/decision.json"

def load_report():
    if not os.path.exists(REPORT_PATH):
        return None
    with open(REPORT_PATH) as f:
        return json.load(f)

def evaluate_signal(report):
    sp = report.get("spectral_profile", {})

    alpha = sp.get("estimated_alpha", 0)
    std = sp.get("bootstrap_std", 1)

    signal_strength = abs(alpha - 0.5) / (std + 1e-9)

    if signal_strength > 5:
        return "STRONG"
    elif signal_strength > 2:
        return "WEAK"
    else:
        return "NO_SIGNAL"

def build_decision(report):
    result = evaluate_signal(report)

    decision = {
        "decision": result,
        "action": None,
        "confidence": None
    }

    if result == "STRONG":
        decision["action"] = "EXPORT_MARKET_SIGNAL"
        decision["confidence"] = "HIGH"

    elif result == "WEAK":
        decision["action"] = "RETEST_WITH_MORE_DATA"
        decision["confidence"] = "MEDIUM"

    else:
        decision["action"] = "REJECT_HYPOTHESIS"
        decision["confidence"] = "LOW"

    return decision

def main():
    report = load_report()
    if report is None:
        print("No report found")
        return

    decision = build_decision(report)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(decision, f, indent=2)

    print("Decision generated:", decision)

if __name__ == "__main__":
    main()
