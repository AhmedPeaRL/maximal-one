import json
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from analysis.json_safe import to_json_safe  # ✅ FIX

ART = "artifacts"


def load(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def load_series():
    path = os.path.join("real-data", "sunspots_global_prepared.csv")
    if not os.path.exists(path):
        return None

    import pandas as pd
    df = pd.read_csv(path)

    if "value" not in df.columns:
        return None

    return df["value"].values


def baseline_model(series):
    X = np.arange(len(series)).reshape(-1, 1)
    y = series

    split = int(0.7 * len(series))

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X[:split], y[:split])

    pred = model.predict(X[split:])
    mse = mean_squared_error(y[split:], pred)

    return float(mse)  # ✅ مهم


def hcm_result():
    path = os.path.join(ART, "chaotic_benchmark.json")
    data = load(path)

    if not data or data.get("skipped", False):
        return None

    return data.get("mse", None)


def main():

    series = load_series()

    if series is None:
        result = {
            "passed": False,
            "reason": "missing_dataset"
        }
    else:
        baseline = baseline_model(series)
        hcm_mse = hcm_result()

        if hcm_mse is None:
            result = {
                "passed": False,
                "reason": "missing_hcm_result"
            }
        else:
            improvement = (baseline - hcm_mse) / baseline

            result = {
                "baseline_mse": float(baseline),
                "hcm_mse": float(hcm_mse),
                "relative_improvement": float(improvement),
                "passed": bool(improvement > 0.1)  # ✅ أهم نقطة
            }

    # ✅ تحويل شامل آمن
    result = to_json_safe(result)

    os.makedirs(ART, exist_ok=True)

    with open(os.path.join(ART, "external_validation.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
