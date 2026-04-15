import json
import time
import hashlib
import os

STATE_PATH = "data/live_field_state.json"
FEEDBACK_PATH = "data/reality_feedback.json"

def load_state():
    if not os.path.exists(STATE_PATH):
        return None
    with open(STATE_PATH) as f:
        return json.load(f)

def load_feedback():
    if not os.path.exists(FEEDBACK_PATH):
        return None
    with open(FEEDBACK_PATH) as f:
        return json.load(f)

def compute_delta(state, feedback):
    try:
        before = state.get("scientific_signal", {}).get("alpha", 0)
        after = feedback.get("observed_alpha", 0)

        delta = after - before
        return {
            "before": before,
            "after": after,
            "delta": delta,
            "effect_detected": abs(delta) > 0.01
        }
    except:
        return {
            "error": "delta_computation_failed"
        }

def build_closure_proof(delta):
    raw = json.dumps(delta, sort_keys=True)
    h = hashlib.sha256(raw.encode()).hexdigest()

    return {
        "timestamp": time.time(),
        "delta": delta,
        "closure_hash": h,
        "status": "closed_loop" if delta.get("effect_detected") else "no_effect"
    }

def save_closure(proof):
    os.makedirs("data", exist_ok=True)
    with open("data/reality_closure.json", "w") as f:
        json.dump(proof, f, indent=2)

def main():
    state = load_state()
    feedback = load_feedback()

    if not state or not feedback:
        print("Missing state or feedback")
        return

    delta = compute_delta(state, feedback)
    proof = build_closure_proof(delta)
    save_closure(proof)

    print("Reality closure loop executed")
    print(json.dumps(proof, indent=2))

if __name__ == "__main__":
    main()
