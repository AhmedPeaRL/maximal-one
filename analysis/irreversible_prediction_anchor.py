import json, time, hashlib, os
from datetime import datetime

PRED_PATH = "data/predictions/"
ANCHOR_PATH = "public/prediction_anchor.json"
SIGNAL_PATH = "artifacts/canonical_report.json"

os.makedirs(PRED_PATH, exist_ok=True)

def load_real_signal():
    if not os.path.exists(SIGNAL_PATH):
        raise RuntimeError("Missing canonical report → cannot generate prediction")

    with open(SIGNAL_PATH) as f:
        report = json.load(f)

    try:
        alpha = report["spectral_profile"]["estimated_alpha"]
        sigma = report["spectral_profile"]["bootstrap_std"]
    except KeyError:
        raise RuntimeError("Invalid report structure")

    return alpha, sigma


def generate_prediction():
    alpha, sigma = load_real_signal()

    prediction = {
        "target": "spectral_alpha_future_window",
        "expected_value": alpha,
        "uncertainty": sigma,
        "confidence": max(0.0, min(1.0, 1 - sigma)),
        "window": "next_run",
        "source": "canonical_report"
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
