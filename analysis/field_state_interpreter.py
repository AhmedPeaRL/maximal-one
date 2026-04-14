import json
import os

def interpret():
    state = {
        "coherence": 0,
        "signals": [],
        "status": "unknown"
    }

    if os.path.exists("artifacts/runtime_divergence.json"):
        state["signals"].append("divergence")

    if os.path.exists("data/live_field_state.json"):
        with open("data/live_field_state.json") as f:
            d = json.load(f)
            state["coherence"] = d.get("field_coherence", 0)

    if state["coherence"] > 0.8:
        state["status"] = "stable"
    elif state["coherence"] > 0.5:
        state["status"] = "transitional"
    else:
        state["status"] = "unstable"

    os.makedirs("public", exist_ok=True)

    with open("public/field_interpretation.json", "w") as f:
        json.dump(state, f, indent=2)

    print("Field interpretation updated.")

if __name__ == "__main__":
    interpret()
