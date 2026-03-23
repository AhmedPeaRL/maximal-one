import numpy as np
import json
from pathlib import Path

ART = Path("artifacts")


def load_series():
    path = Path("real-data/sunspots_global_prepared.csv")
    if not path.exists():
        return None

    import pandas as pd
    df = pd.read_csv(path)
    return df.values.squeeze()


# -----------------------------
# Non-trivial prediction test
# -----------------------------

def rolling_prediction_score(series, window=10):
    preds = []
    actuals = []

    for i in range(window, len(series) - 1):
        past = series[i-window:i]
        pred = np.mean(past)  # simple non-trivial baseline
        preds.append(pred)
        actuals.append(series[i+1])

    return np.corrcoef(preds, actuals)[0, 1]


def shuffled_score(series):
    s = np.copy(series)
    np.random.shuffle(s)
    return rolling_prediction_score(s)


# -----------------------------
# Core
# -----------------------------

def run_test(series, trials=20):

    real = rolling_prediction_score(series)

    surr = []
    for _ in range(trials):
        surr.append(shuffled_score(series))

    surr = np.array(surr)

    z = (real - np.mean(surr)) / (np.std(surr) + 1e-9)

    return {
        "real_score": float(real),
        "surrogate_mean": float(np.mean(surr)),
        "surrogate_std": float(np.std(surr)),
        "z_score": float(z),
        "non_trivial": bool(z > 2.5)
    }


def main():

    series = load_series()

    if series is None or len(series) < 300:
        result = {"skipped": True}
    else:
        result = run_test(series)

    ART.mkdir(exist_ok=True)
    (ART / "reality_gap_hardener.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
