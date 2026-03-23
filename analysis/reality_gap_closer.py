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
# Random surrogate generator
# -----------------------------

def generate_surrogate(series):
    shuffled = np.copy(series)
    np.random.shuffle(shuffled)
    return shuffled


# -----------------------------
# Simple predictive structure test
# -----------------------------

def predictive_score(series):
    x = series[:-1]
    y = series[1:]
    return np.corrcoef(x, y)[0, 1]


# -----------------------------
# Core test
# -----------------------------

def run_test(series, trials=20):

    real_score = predictive_score(series)

    surrogate_scores = []

    for _ in range(trials):
        surr = generate_surrogate(series)
        score = predictive_score(surr)
        surrogate_scores.append(score)

    surrogate_scores = np.array(surrogate_scores)

    mean_surr = np.mean(surrogate_scores)
    std_surr = np.std(surrogate_scores)

    z_score = (real_score - mean_surr) / (std_surr + 1e-9)

    return {
        "real_score": float(real_score),
        "surrogate_mean": float(mean_surr),
        "surrogate_std": float(std_surr),
        "z_score": float(z_score),
        "beyond_random": bool(z_score > 2.5)
    }


# -----------------------------
# Main
# -----------------------------

def main():

    series = load_series()

    if series is None or len(series) < 300:
        result = {"skipped": True}
    else:
        result = run_test(series)

    ART.mkdir(exist_ok=True)
    (ART / "reality_gap_closer.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
