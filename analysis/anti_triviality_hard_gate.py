import numpy as np
import pandas as pd
import json
import sys
from pathlib import Path
import time
START_TIME = time.time()
MAX_RUNTIME = 300  # seconds

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ART = Path("artifacts")

# -----------------------------
# Load series
# -----------------------------

def load_series():
    path = Path("real-data/sunspots_global_prepared.csv")
    if not path.exists():
        return None

    df = pd.read_csv(path)
    return df.values.squeeze()

# -----------------------------
# HARD transformations
# -----------------------------

def difference(series):
    return np.diff(series)

def phase_scramble(series):
    fft = np.fft.rfft(series)
    phases = np.angle(fft)
    magnitudes = np.abs(fft)

    random_phases = np.random.uniform(-np.pi, np.pi, size=len(phases))
    scrambled = magnitudes * np.exp(1j * random_phases)

    return np.fft.irfft(scrambled, n=len(series))

# -----------------------------
# predictors
# -----------------------------

def persistence(history):
    return history[-1]
from analysis.hcm_state_predictor import HCMStatePredictor
from analysis.hcm_dynamical_predictor import HCMDynamicalPredictor
from analysis.hcm_invariant_predictor import HCMInvariantPredictor
from analysis.hcm_robust_predictor import HCMRobustPredictor

models = [
    HCMStatePredictor(),
    HCMDynamicalPredictor(),
    HCMInvariantPredictor(),
    HCMRobustPredictor()
]

def hcm_predict(history):
    preds = []
    for m in models:
        try:
            preds.append(m.predict(history))
        except:
            preds.append(history[-1])
    return float(np.median(preds))
    
# -----------------------------
# evaluation
# -----------------------------

def rolling_mse(series, model, max_steps=300):

    split = int(len(series)*0.7)
    train = list(series[:split])
    test = series[split:]

    if time.time() - START_TIME > MAX_RUNTIME:
        break

    # 🔥 NEW: limit steps
    if len(test) > max_steps:
        test = test[:max_steps]

    history = train.copy()
    preds = []

    for t in range(len(test)):
        preds.append(model(history))
        history.append(test[t])

    return float(np.mean((np.array(test) - np.array(preds))**2))

# -----------------------------
# core
# -----------------------------

def evaluate(series):
    # 🔥 NEW: downsample لو كبير
    if len(series) > 2000:
        idx = np.linspace(0, len(series)-1, 2000).astype(int)
        series = series[idx]

    tests = {}

    # original
    tests["original"] = series

    # diff
    tests["diff"] = difference(series)
 
    # scramble
    tests["phase"] = phase_scramble(series)

    results = {}

    for name, s in tests.items():

        if len(s) < 100:
            continue

        mse_p = rolling_mse(s, persistence)
        mse_h = rolling_mse(s, hcm_predict)

        results[name] = {
            "persistence_mse": mse_p,
            "hcm_mse": mse_h,
            "hcm_better": mse_h < mse_p
        }

    return results


def main():

    series = load_series()

    if series is None:
        result = {"skipped": True}
    else:
        result = evaluate(series)

        # pass condition: HCM wins in at least 2 hard regimes
        wins = sum(1 for r in result.values() if r["hcm_better"])

        result["hard_non_trivial"] = (
            wins >= 2 and 
            result.get("diff", {}).get("hcm_better", False)
        )

    ART.mkdir(exist_ok=True)
    (ART / "anti_triviality_hard.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
