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


# -----------------------------
# Advanced entropy (multi-scale)
# -----------------------------

def multiscale_entropy(series, scales=[1,2,3,5]):
    def coarse_grain(s, scale):
        n = len(s) // scale
        return np.array([np.mean(s[i*scale:(i+1)*scale]) for i in range(n)])

    entropies = []
    for s in scales:
        cg = coarse_grain(series, s)
        hist, _ = np.histogram(cg, bins=50, density=True)
        hist = hist + 1e-12
        entropies.append(-np.sum(hist * np.log(hist)))

    return np.mean(entropies)


# -----------------------------
# Nonlinear autocorrelation
# -----------------------------

def nonlinear_autocorr(series, lag):
    x = series[:-lag]
    y = series[lag:]
    return np.corrcoef(np.square(x), y)[0,1]


# -----------------------------
# Phase-space consistency
# -----------------------------

def phase_space_score(series, delay=2):
    x = series[:-delay]
    y = series[delay:]
    return np.mean(np.abs(x - y))


# -----------------------------
# Structural score (enhanced)
# -----------------------------

def structural_score(series):

    entropy = multiscale_entropy(series)

    ac1 = np.corrcoef(series[:-1], series[1:])[0,1]
    ac5 = np.corrcoef(series[:-5], series[5:])[0,1]

    nonlin = nonlinear_autocorr(series, 2)
    phase = phase_space_score(series)

    score = (
        entropy * (abs(ac1) + abs(ac5)) +
        abs(nonlin) +
        (1.0 / (1.0 + phase))
    )

    return float(score)


# -----------------------------
# Evaluation
# -----------------------------

def evaluate_models(series):

    ar_score = structural_score(series)

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


# -----------------------------
# Main
# -----------------------------

def main():

    series = load_series()

    if series is None or len(series) < 300:
        result = {"skipped": True}
    else:
        ar_score, hcm_score = evaluate_models(series)

        diff = hcm_score - ar_score

        result = {
            "ar_structural": float(ar_score),
            "hcm_structural": float(hcm_score),
            "delta": float(diff),
            "relative_gain": float(diff / (abs(ar_score) + 1e-9)),
            "hcm_superior": bool(diff > 0.01),
            "type": "structural_intelligence"
        }

    ART.mkdir(exist_ok=True)
    (ART / "structural_test.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
