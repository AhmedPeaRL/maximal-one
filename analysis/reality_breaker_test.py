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
# Controlled destruction
# -----------------------------

def partial_shuffle(series, ratio=0.3):
    s = np.copy(series)
    n = len(s)
    idx = np.random.choice(n, int(n * ratio), replace=False)
    shuffled = np.copy(s[idx])
    np.random.shuffle(shuffled)
    s[idx] = shuffled
    return s


def predictive_score(series):
    x = series[:-1]
    y = series[1:]
    return np.corrcoef(x, y)[0, 1]


# -----------------------------
# Core test
# -----------------------------

def run_test(series, trials=10):

    original = predictive_score(series)

    degraded_scores = []

    for _ in range(trials):
        corrupted = partial_shuffle(series, ratio=0.3)
        score = predictive_score(corrupted)
        degraded_scores.append(score)

    degraded_scores = np.array(degraded_scores)

    drop = original - np.mean(degraded_scores)

    return {
        "original_score": float(original),
        "degraded_mean": float(np.mean(degraded_scores)),
        "drop": float(drop),
        "robust": bool(drop > 0.05)
    }


def main():

    series = load_series()

    if series is None or len(series) < 300:
        result = {"skipped": True}
    else:
        result = run_test(series)

    ART.mkdir(exist_ok=True)
    (ART / "reality_breaker.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
