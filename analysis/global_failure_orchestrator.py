import os
import json
import sys
import time
import hashlib

FAILURE_LOG = "artifacts/global_failure_log.json"
STATE_FILE = "artifacts/global_state.json"


def safe_load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default


def record_failure(stage, severity, message):
    data = safe_load(FAILURE_LOG, [])

    entry = {
        "timestamp": time.time(),
        "stage": stage,
        "severity": severity,
        "message": message
    }

    data.append(entry)

    with open(FAILURE_LOG, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[GFCL] Failure recorded: {stage} → {severity}")


def evaluate_system_state():
    data = safe_load(FAILURE_LOG, [])

    critical = [f for f in data if f["severity"] == "critical"]
    high = [f for f in data if f["severity"] == "high"]

    if len(critical) > 0:
        return "compromised"

    if len(high) > 3:
        return "unstable"

    return "stable"


def seal_if_needed(state):
    if state == "compromised":
        print("[GFCL] SYSTEM COMPROMISED → HARD STOP")

        # kill pipeline truth propagation
        if os.path.exists("public/live_truth.json"):
            os.remove("public/live_truth.json")

        with open("artifacts/SEALED", "w") as f:
            f.write("SYSTEM SEALED DUE TO CRITICAL FAILURE")

        sys.exit(1)


def generate_fingerprint():
    data = safe_load(FAILURE_LOG, [])
    raw = json.dumps(data, sort_keys=True)

    return hashlib.sha256(raw.encode()).hexdigest()


def main():
    state = evaluate_system_state()

    fingerprint = generate_fingerprint()

    out = {
        "timestamp": time.time(),
        "state": state,
        "failure_fingerprint": fingerprint
    }

    os.makedirs("artifacts", exist_ok=True)

    with open(STATE_FILE, "w") as f:
        json.dump(out, f, indent=2)

    print(f"[GFCL] STATE = {state}")
    print(f"[GFCL] fingerprint = {fingerprint}")

    seal_if_needed(state)


if __name__ == "__main__":
    main()
