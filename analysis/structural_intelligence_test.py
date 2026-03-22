import numpy as np
import json
import sys
from pathlib import Path

ART = Path("artifacts")


def load_series():
    path = Path("real-data/sunspots_global_prepared.csv")
    if not path.exists():
        return None

    import pandas as pd
    df = pd.read_csv(path)
    return df.values.squeeze()


def compute_entropy(series):
    hist, _ = np.histogram(series, bins=50, density=True)
    hist = hist + 1e-12
    return -np.sum(hist * np.log(hist))


def autocorr(series, lag=1):
    return np.corrcoef(series[:-lag], series[lag:])[0,1]


def structural_score(series):

    entropy = compute_entropy(series)

    ac1 = autocorr(series, 1)
    ac5 = autocorr(series, 5)

    complexity = entropy * (abs(ac1) + abs(ac5))

    return float(complexity)


def evaluate_models(series):

    # baseline: AR-like naive
    ar_score = structural_score(series)

    # ensure root path is visible
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))
  
    from analysis.hcm_state_predictor import HCMStatePredictor

    model = HCMStatePredictor(embed_dim=4, delay=2, k=6)
    model.fit(series)

    reconstructed = []
    history = list(series[:50])

    for i in range(50, len(series)):
        pred = model.predict(history)
        reconstructed.append(pred)
        history.append(series[i])

    reconstructed = np.array(reconstructed)

    hcm_score = structural_score(reconstructed)

    return ar_score, hcm_score


def main():

    series = load_series()

    if series is None or len(series) < 300:
        result = {
            "skipped": True
        }
    else:
        ar_score, hcm_score = evaluate_models(series)

        result = {
            "ar_structural": float(ar_score),
            "hcm_structural": float(hcm_score),
            "hcm_superior": bool(hcm_score > ar_score),
            "type": "structural_intelligence"
        }

    ART.mkdir(exist_ok=True)
    (ART / "structural_test.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
