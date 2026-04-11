import json
import time
import hashlib
import os

OUT = "artifacts/pre_registration.json"

def generate_prediction():
    # deterministic pseudo-prediction based on time slice
    t = int(time.time() // 3600)  # hourly bucket
    
    prediction = {
        "timestamp": t,
        "expected_alpha_range": [0.48, 0.54],
        "expected_structure": "weak_periodic_or_none",
        "confidence": 0.6
    }

    return prediction

def sign(prediction):
    raw = json.dumps(prediction, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()

def main():
    pred = generate_prediction()
    pred["signature"] = sign(pred)

    os.makedirs("artifacts", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(pred, f, indent=2)

    print("Pre-registration locked.")
    print(json.dumps(pred, indent=2))

if __name__ == "__main__":
    main()
