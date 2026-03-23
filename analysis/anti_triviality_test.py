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
# Baseline predictors
# -----------------------------

def naive_shift(series):
    return series[:-1], series[1:]


def moving_average(series, window=5):
    preds = []
    actuals = []

    for i in range(window, len(series) - 1):
        preds.append(np.mean(series[i-window:i]))
        actuals.append(series[i+1])

    return np.array(preds), np.array(actuals)


def random_predictor(series):
    x = series[:-1]
    y = np.random.permutation(series[1:])
    return x, y


def score(x, y):
    return np.corrcoef(x, y)[0, 1]


# -----------------------------
# Core comparison
# -----------------------------

def run_test(series):

    # naive
    x1, y1 = naive_shift(series)
    naive_score = score(x1, y1)

    # moving avg
    x2, y2 = moving_average(series)
    ma_score = score(x2, y2)

    # random baseline
    x3, y3 = random_predictor(series)
    rand_score = score(x3, y3)

    return {
        "naive_score": float(naive_score),
        "moving_average_score": float(ma_score),
        "random_score": float(rand_score),
        "non_trivial": bool(
            naive_score < 0.95 and
            ma_score < 0.95
        )
    }


def main():

    series = load_series()

    if series is None or len(series) < 300:
        result = {"skipped": True}
    else:
        result = run_test(series)

    ART.mkdir(exist_ok=True)
    (ART / "anti_triviality.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
