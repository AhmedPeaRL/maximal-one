import json
import time
import hashlib
import os
from datetime import datetime

STATE_FILE = "data/latest_state.json"
OUTPUT_DIR = "data/autonomous"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"field": "unknown", "layer": "unknown"}
    with open(STATE_FILE) as f:
        return json.load(f)

def generate_witness(state):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "field": state.get("field", "unknown"),
        "layer": state.get("layer", "unknown"),
        "origin": "autonomous",
        "intent": "self-observation",
    }

    raw = json.dumps(payload, sort_keys=True)
    payload["hash"] = hashlib.sha256(raw.encode()).hexdigest()

    return payload

def persist(payload):
    fname = f"{OUTPUT_DIR}/auto_{int(time.time())}.json"
    with open(fname, "w") as f:
        json.dump(payload, f, indent=2)

    print("Autonomous witness stored:", fname)

if __name__ == "__main__":
    state = load_state()
    witness = generate_witness(state)
    persist(witness)
