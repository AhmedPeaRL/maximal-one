import json
import os
import math

REPORT_PATH = "artifacts/canonical_report.json"
HISTORY_PATH = "data/decision_history.json"
OUTPUT_PATH = "artifacts/decision.json"
PRESSURE_PATH = "artifacts/external_pressure.json"

with open("core-scientific/decision_contract/decision_contract.json") as f:
    CONTRACT = json.load(f)


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ✅ FIX: pressure becomes explicit signal (not hidden side-effect)
def load_pressure():
    pressure = load_json(PRESSURE_PATH)

    if not pressure:
        return {
            "status": "absent",
            "score": 0
        }

    try:
        status = pressure.get("evaluation", {}).get("status", "unknown")

        score_map = {
            "stable": 0,
            "warning": 1,
            "critical": 2
        }

        return {
            "status": status,
            "score": score_map.get(status, 0)
        }

    except Exception:
        return {
            "status": "corrupted",
            "score": 1
        }


def compute_signal(report):
    sp = report.get("spectral_profile", {})

    alpha = sp.get("estimated_alpha", 0.5)
    std = sp.get("bootstrap_std", 1e-6)

    expected = 1.0  # neutral scaling baseline

    z = abs(alpha - expected) / (std + 1e-9)

    return {
        "alpha": alpha,
        "std": std,
        "z_score": z
    }


def bayesian_confidence(z):
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


# ✅ FIX: decision depends on BOTH signal + pressure
def build_decision(signal, pressure):
    z = signal["z_score"]
    confidence = bayesian_confidence(z)

    history = load_history()
    persistent = detect_persistence(z, history)

    # 🔴 pressure override
    if pressure["score"] >= 2:
        return "UNSTABLE_UNDER_PRESSURE", "HALT_AND_DIAGNOSE", confidence

    if z > 5 and persistent:
        return "STRONG_PERSISTENT", "EXPORT_MARKET_SIGNAL", confidence

    elif z > 3:
        return "STRONG", "RETEST_FAST", confidence

    elif z > 2:
        return "WEAK", "COLLECT_MORE_DATA", confidence

    else:
        return "NO_SIGNAL", "REJECT_HYPOTHESIS", confidence


def enforce_decision(decision, signals):
    rules = CONTRACT["binding_rules"]

    if rules["reproducibility_required"] and not signals.get("reproducible"):
        return "rejected"

    if rules["falsifiability_required"] and not signals.get("falsifiable"):
        return "rejected"

    if rules["external_anchor_required"] and not signals.get("externally_anchored"):
        return "unstable"

    return decision


def main():
    report = load_json(REPORT_PATH)

    if report is None:
        print("No report.")
        return

    signal = compute_signal(report)

    # ✅ FIX: explicit pressure load
    pressure = load_pressure()

    label, action, conf = build_decision(signal, pressure)

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
