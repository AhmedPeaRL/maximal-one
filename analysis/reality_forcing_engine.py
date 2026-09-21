from __future__ import annotations

import hashlib
import json
import random
import time
from pathlib import Path


PREDICTION_FILE = Path(
    "artifacts/reality_prediction.json"
)

RESULT_FILE = Path(
    "artifacts/reality_result.json"
)

SEED = 42

def deterministic_synthetic_series_value(t: int) -> float:
    rng = random.Random(SEED + int(t))

    base = 30000.0
    noise = rng.uniform(-500.0, 500.0)
    trend = (t % 10) * 50.0

    return base + trend + noise

def generate_synthetic_prediction():
    timestamp = int(time.time())

    reference_value = (
        deterministic_synthetic_series_value(
            timestamp
        )
    )

    prediction = {
        "timestamp": timestamp,
        "prediction": (
            "up"
            if reference_value % 2 > 1
            else "down"
        ),
        "reference_value": reference_value,
        "data_role": "synthetic_simulation",
        "real_world_claim": False,
    }

    canonical = json.dumps(
        prediction,
        sort_keys=True
    ).encode("utf-8")

    prediction["hash"] = hashlib.sha256(
        canonical
    ).hexdigest()

    PREDICTION_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    PREDICTION_FILE.write_text(
        json.dumps(
            prediction,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8",
    )

    return prediction

def evaluate_synthetic_prediction(prediction):
    time.sleep(2)

    timestamp = int(time.time())

    new_value = (
        deterministic_synthetic_series_value(
            timestamp
        )
    )

    actual = (
        "up"
        if new_value > prediction["reference_value"]
        else "down"
    )

    result = {
        "prediction": prediction["prediction"],
        "actual": actual,
        "correct": (
            prediction["prediction"] == actual
        ),
        "initial_value": prediction[
            "reference_value"
        ],
        "final_value": new_value,
        "timestamp": timestamp,
        "data_role": "synthetic_simulation",
        "real_world_claim": False,
        "interpretation": (
            "This is a deterministic synthetic "
            "simulation only. It is not evidence "
            "of real-world prediction."
        ),
    }

    RESULT_FILE.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8",
    )

    return result

def main():
    prediction = generate_synthetic_prediction()
    result = evaluate_synthetic_prediction(
        prediction
    )

    print(
        json.dumps(
            {
                "prediction": prediction,
                "result": result,
            },
            indent=2
        )
    )

if __name__ == "__main__":
    main()
