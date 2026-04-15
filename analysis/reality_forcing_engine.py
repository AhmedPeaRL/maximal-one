import json
import time
import hashlib
import requests
import os

PREDICTION_FILE = "artifacts/reality_prediction.json"
RESULT_FILE = "artifacts/reality_result.json"

EXTERNAL_API = "https://api.coindesk.com/v1/bpi/currentprice.json"


def generate_prediction():
    # مثال بسيط: اتجاه سعر BTC
    r = requests.get(EXTERNAL_API, timeout=10).json()
    price = float(r["bpi"]["USD"]["rate"].replace(",", ""))

    prediction = {
        "timestamp": time.time(),
        "prediction": "up" if price % 2 > 1 else "down",  # toy logic
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

    time.sleep(5)  # simulate delay (replace with real scheduling later)

    r = requests.get(EXTERNAL_API, timeout=10).json()
    new_price = float(r["bpi"]["USD"]["rate"].replace(",", ""))

    actual = "up" if new_price > pred["reference_price"] else "down"

    result = {
        "prediction": pred["prediction"],
        "actual": actual,
        "correct": pred["prediction"] == actual,
        "initial_price": pred["reference_price"],
        "final_price": new_price,
        "timestamp": time.time()
    }

    with open(RESULT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("Reality evaluated:", result)


if __name__ == "__main__":
    generate_prediction()
    evaluate_prediction()
