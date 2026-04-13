import json
import os
import time
import hashlib

STATE_PATH = "data/live_field_state.json"
TRUTH_PATH = "public/live_truth.json"
FEEDBACK_PATH = "data/causal_feedback.json"


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


# 🔒 enforce numeric safety
def to_float(x, default=0.0):
    try:
        if x is None:
            return default
        return float(x)
    except (ValueError, TypeError):
        return default


def compute_feedback(state, truth):
    signal = truth.get("scientific_signal", {})

    # 🔥 SAFE extraction
    confidence = to_float(signal.get("confidence", 0))
    coherence = to_float(state.get("field_coherence", 0))

    drift = 1.0 - coherence

    decision = truth.get("decision", {}).get("global", "unknown")

    feedback = {
        "timestamp": time.time(),
        "confidence": confidence,
        "coherence": coherence,
        "drift": drift,
        "decision": decision,
        "action": None
    }

    # 🔥 core logic (safe now)
    if confidence > 0.9 and drift < 0.2:
        feedback["action"] = "reinforce"
    elif drift > 0.4:
        feedback["action"] = "correct"
    else:
        feedback["action"] = "observe"

    return feedback


def persist_feedback(feedback):
    os.makedirs("data", exist_ok=True)

    with open(FEEDBACK_PATH, "w") as f:
        json.dump(feedback, f, indent=2)

    h = hashlib.sha256(json.dumps(feedback).encode()).hexdigest()

    with open(FEEDBACK_PATH + ".hash", "w") as f:
        f.write(h)

    print("Feedback stored:", h)


if __name__ == "__main__":
    state = load_json(STATE_PATH)
    truth = load_json(TRUTH_PATH)

    feedback = compute_feedback(state, truth)
    persist_feedback(feedback)
