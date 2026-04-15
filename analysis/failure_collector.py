import json
import os
import time

FAILURE_LOG = "artifacts/failure_log.json"


def load():
    if not os.path.exists(FAILURE_LOG):
        return []
    with open(FAILURE_LOG) as f:
        return json.load(f)


def save(data):
    os.makedirs("artifacts", exist_ok=True)
    with open(FAILURE_LOG, "w") as f:
        json.dump(data, f, indent=2)


def record(step, error, severity="medium"):
    data = load()

    entry = {
        "timestamp": time.time(),
        "step": step,
        "error": str(error),
        "severity": severity
    }

    data.append(entry)

    # keep last 200
    data = data[-200:]

    save(data)

    print(f"[FAILURE LOGGED] {step} → {severity}")


if __name__ == "__main__":
    import sys

    step = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    error = sys.argv[2] if len(sys.argv) > 2 else "no_error"

    record(step, error)
