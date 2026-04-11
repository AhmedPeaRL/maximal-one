import json
import hashlib
import time
import os

LOCK_PATH = "artifacts/prediction_lock.json"


def create_lock(predictions):
    payload = {
        "predictions": predictions,
        "timestamp": time.time()
    }

    raw = json.dumps(payload, sort_keys=True)
    signature = hashlib.sha256(raw.encode()).hexdigest()

    payload["signature"] = signature

    with open(LOCK_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print("Prediction lock created:", signature)


def verify_lock(current_predictions):
    if not os.path.exists(LOCK_PATH):
        print("No lock found.")
        return False

    with open(LOCK_PATH) as f:
        locked = json.load(f)

    raw = json.dumps({
        "predictions": locked["predictions"],
        "timestamp": locked["timestamp"]
    }, sort_keys=True)

    expected = hashlib.sha256(raw.encode()).hexdigest()

    if expected != locked["signature"]:
        print("Lock integrity violated.")
        return False

    if current_predictions != locked["predictions"]:
        print("Prediction drift detected.")
        return False

    print("Prediction lock verified.")
    return True


if __name__ == "__main__":
    test_predictions = {
        "alpha_expected": 0.5,
        "sigma_expected": 0.02
    }

    create_lock(test_predictions)
