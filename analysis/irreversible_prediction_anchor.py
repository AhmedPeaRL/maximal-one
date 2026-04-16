import json, time, hashlib, os
from datetime import datetime

PRED_PATH = "data/predictions/"
ANCHOR_PATH = "public/prediction_anchor.json"

os.makedirs(PRED_PATH, exist_ok=True)

def generate_prediction():
    """
    هنا النظام بيولد تنبؤ حقيقي
    تقدر تربطه بأي signal عندك (spectral / attractor / universality)
    """

    # مثال بسيط (تستبدله بالـ real signal بتاعك)
    prediction = {
        "target": "sunspots_next_peak",
        "expected_value": 135.0,
        "confidence": 0.82,
        "window": "next_6_months"
    }

    return prediction


def anchor_prediction(pred):
    timestamp = time.time()

    raw = json.dumps(pred, sort_keys=True)
    h = hashlib.sha256(raw.encode()).hexdigest()

    record = {
        "timestamp": timestamp,
        "datetime": datetime.utcnow().isoformat(),
        "prediction": pred,
        "hash": h,
        "status": "locked"
    }

    fname = f"{PRED_PATH}prediction_{int(timestamp)}.json"
    with open(fname, "w") as f:
        json.dump(record, f, indent=2)

    with open(ANCHOR_PATH, "w") as f:
        json.dump(record, f, indent=2)

    print("Prediction anchored:", h)


if __name__ == "__main__":
    p = generate_prediction()
    anchor_prediction(p)
