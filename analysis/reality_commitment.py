import json
import time
import os
import hashlib
import random

OUTPUT_PATH = "data/reality_commitments.json"

def generate_prediction():
    # مثال بسيط – تقدر تربطه بأي signal حقيقي عندك
    prediction = {
        "id": hashlib.sha256(str(time.time()).encode()).hexdigest(),
        "timestamp": int(time.time()),
        "target_metric": "alpha",
        "predicted_value": round(random.uniform(0.45, 0.6), 3),
        "tolerance": 0.05,
        "evaluation_after_seconds": 3600  # ساعة
    }
    return prediction

def store_prediction(pred):
    os.makedirs("data", exist_ok=True)

    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(pred)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print("Prediction committed:", pred["id"])

if __name__ == "__main__":
    p = generate_prediction()
    store_prediction(p)
