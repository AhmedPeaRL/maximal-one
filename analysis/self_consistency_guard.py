import json
import os
import hashlib
import time

STATE_PATH = "data/live_field_state.json"
LOG_PATH = "data/self_consistency_log.json"

def hash_state(state):
    return hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()

def load_state():
    if not os.path.exists(STATE_PATH):
        return None
    with open(STATE_PATH) as f:
        return json.load(f)

def load_log():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH) as f:
        return json.load(f)

def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def main():
    state = load_state()
    if not state:
        print("No state found")
        return

    log = load_log()

    current_hash = hash_state(state)

    if log:
        last_hash = log[-1]["hash"]

        if last_hash != current_hash:
            print("⚠️ State drift detected")

    log.append({
        "timestamp": time.time(),
        "hash": current_hash,
        "state": state
    })

    save_log(log)

    print("Self-consistency recorded")

if __name__ == "__main__":
    main()
