import json
import time
import hashlib
import os
import random

PREDICTION_FILE = "artifacts/reality_prediction.json"
RESULT_FILE = "artifacts/reality_result.json"

SEED = 42  # deterministic anchor


def deterministic_price(t):
    random.seed(SEED + int(t))
    base = 30000
    noise = random.uniform(-500, 500)
    trend = (t % 10) * 50
    return base + trend + noise


def generate_prediction():
    t = int(time.time())

    price = deterministic_price(t)

    prediction = {
        "timestamp": t,
        "prediction": "up" if price % 2 > 1 else "down",
        "reference_price": price
    }

    raw = json.dumps(prediction, sort_keys=True).encode()
    prediction["hash"] = hashlib.sha256(raw).hexdigest()

    os.makedirs("artifacts", exist_ok=True)

    with open(PREDICTION_FILE, "w") as f:
        json.dump(prediction, f, indent=2)

    print("Prediction committed:", prediction["hash"])


def evaluate_prediction():
    if not os.path.exists(PREDICTION_FILE):
        print("No prediction found")
        return

    with open(PREDICTION_FILE) as f:
        pred = json.load(f)

    time.sleep(2)

    t_new = int(time.time())
    new_price = deterministic_price(t_new)

    actual = "up" if new_price > pred["reference_price"] else "down"

    result = {
        "prediction": pred["prediction"],
        "actual": actual,
        "correct": pred["prediction"] == actual,
        "initial_price": pred["reference_price"],
        "final_price": new_price,
        "timestamp": t_new
    }

    with open(RESULT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("Reality evaluated:", result)


if __name__ == "__main__":
    generate_prediction()
    evaluate_prediction()
