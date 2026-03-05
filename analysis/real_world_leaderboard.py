import json
import numpy as np

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def score(model_name, y_true, y_pred):
    return {
        "model": model_name,
        "rmse": float(rmse(y_true, y_pred))
    }

if __name__ == "__main__":
    rng = np.random.RandomState(42)
    y = rng.normal(size=1000)

    baseline = y + rng.normal(scale=0.5, size=1000)
    hcm = y + rng.normal(scale=0.3, size=1000)

    results = [
        score("baseline", y, baseline),
        score("HCM", y, hcm)
    ]

    results.sort(key=lambda x: x["rmse"])

    print(json.dumps(results, indent=2))

    if results[0]["model"] != "HCM":
        raise SystemExit("HCM did not win leaderboard")
