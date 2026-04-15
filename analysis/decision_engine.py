import json
import os
import math

REPORT_PATH = "artifacts/canonical_report.json"
HISTORY_PATH = "data/decision_history.json"
OUTPUT_PATH = "artifacts/decision.json"


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def pressure_oracle(data):
    try:
      with open("artifacts/external_pressure.json") as f:
          pressure = json.load(f)

      if pressure["evaluation"]["status"] == "critical":
          decision["global"] = "unstable_under_pressure"
    except:
        pass
    

def compute_signal(report):
    sp = report.get("spectral_profile", {})

    alpha = sp.get("estimated_alpha", 0.5)
    std = sp.get("bootstrap_std", 1e-6)

    z = abs(alpha - 0.5) / std

    return {
        "alpha": alpha,
        "std": std,
        "z_score": z
    }


def bayesian_confidence(z):
    # تحويل z-score لتقدير احتمالي
    return 1 - math.exp(-z)


def load_history():
    h = load_json(HISTORY_PATH)
    return h if h else []


def update_history(entry):
    h = load_history()
    h.append(entry)

    if len(h) > 100:
        h = h[-100:]

    save_json(HISTORY_PATH, h)


def detect_persistence(z, history):
    if len(history) < 5:
        return False

    recent = [h["z"] for h in history[-5:]]
    return all(v > 2 for v in recent)


def build_decision(signal):
    z = signal["z_score"]
    confidence = bayesian_confidence(z)

    history = load_history()
    persistent = detect_persistence(z, history)

    if z > 5 and persistent:
        return "STRONG_PERSISTENT", "EXPORT_MARKET_SIGNAL", confidence

    elif z > 3:
        return "STRONG", "RETEST_FAST", confidence

    elif z > 2:
        return "WEAK", "COLLECT_MORE_DATA", confidence

    else:
        return "NO_SIGNAL", "REJECT_HYPOTHESIS", confidence


def main():
    report = load_json(REPORT_PATH)

    if report is None:
        print("No report.")
        return

    signal = compute_signal(report)

    label, action, conf = build_decision(signal)

    decision = {
        "pressure": pressure,
        "decision": label,
        "action": action,
        "confidence": round(conf, 4),
        "signal": signal
    }

    update_history({
        "z": signal["z_score"]
    })

    save_json(OUTPUT_PATH, decision)

    print("Decision:", decision)


if __name__ == "__main__":
    main()
