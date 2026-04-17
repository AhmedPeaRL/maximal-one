import json
import os
import time

STATE_PATH = "data/adaptive_state.json"
REPORT_PATH = "artifacts/canonical_report.json"

def load_report():
    try:
        with open(REPORT_PATH) as f:
            return json.load(f)
    except:
        return None

def load_state():
    if not os.path.exists(STATE_PATH):
        return {
            "history": [],
            "weights": {
                "alpha": 1.0,
                "sigma": 1.0,
                "confidence": 1.0
            }
        }
    with open(STATE_PATH) as f:
        return json.load(f)

def save_state(state):
    os.makedirs("data", exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

def adapt_weights(signal, state):
    alpha = signal.get("alpha")
    sigma = signal.get("sigma")
    confidence = signal.get("confidence")

    if alpha is None or sigma is None:
        return state

    # 🔥 adaptive logic
    if sigma > 0.2:
        state["weights"]["sigma"] *= 1.1
    else:
        state["weights"]["sigma"] *= 0.95

    if confidence < 0.6:
        state["weights"]["confidence"] *= 1.2
    else:
        state["weights"]["confidence"] *= 0.9

    if alpha < 0.5:
        state["weights"]["alpha"] *= 1.05
    else:
        state["weights"]["alpha"] *= 0.97

    return state

def extract_signal(report):
    try:
        return {
            "alpha": report["spectral_profile"]["estimated_alpha"],
            "sigma": report["spectral_profile"]["bootstrap_std"],
            "confidence": max(0.0, min(1.0, 1 - report["spectral_profile"]["bootstrap_std"]))
        }
    except:
        return {}

def main():
    report = load_report()
    if not report:
        print("No report found")
        return

    state = load_state()
    signal = extract_signal(report)

    state = adapt_weights(signal, state)

    state["history"].append({
        "timestamp": time.time(),
        "signal": signal,
        "weights": state["weights"]
    })

    save_state(state)

    print("Adaptive state updated:", state["weights"])

if __name__ == "__main__":
    main()
