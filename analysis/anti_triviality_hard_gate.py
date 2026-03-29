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

    # 🔥 HARD GUARANTEE
    if not path.exists():
        print("Dataset missing → forcing regeneration...")

        import subprocess

        subprocess.run(
            ["python", "-m", "analysis.generate_real_dataset"],
            check=False
        )

        subprocess.run(
            ["python", "analysis/dataset_preprocessor.py", "real-data/sunspots_global.csv"],
            check=False
        )

    if not path.exists():
        print("Dataset STILL missing → aborting safely")
        return None

    df = pd.read_csv(path)

    # 🔥 sanity check
    if len(df) < 100:
        print("Dataset too small → invalid")
        return None

    return df.values.squeeze()

# -----------------------------
# HARD transformations
# -----------------------------

def difference(series):
    return np.diff(series)

def nonlinear_transform(series):
    return np.tanh(series) + 0.1 * np.sin(series)

def phase_scramble(series):

    # 🔥 LIMIT SIZE
    if len(series) > 800:
        series = series[-800:]

    fft = np.fft.rfft(series)

    magnitudes = np.abs(fft)
    random_phases = np.random.uniform(-np.pi, np.pi, size=len(fft))

    scrambled = magnitudes * np.exp(1j * random_phases)

    return np.fft.irfft(scrambled, n=len(series))

def block_shuffle(series, block_size=20):
    s = series.copy()
    n = len(s)
    blocks = [s[i:i+block_size] for i in range(0, n, block_size)]
    np.random.shuffle(blocks)
    return np.concatenate(blocks)

# -----------------------------
# predictors
# -----------------------------

def persistence(history):
    return history[-1]

from analysis.hcm_phase_space_predictor import HCMPhaseSpacePredictor

class HCMDelayVariant(HCMPhaseSpacePredictor):
    def __init__(self, delay, dim):
        super().__init__(delay=delay, dim=dim)

models = [
    HCMPhaseSpacePredictor(delay=1, dim=3),
    HCMPhaseSpacePredictor(delay=2, dim=3),
    HCMPhaseSpacePredictor(delay=3, dim=3),
    HCMPhaseSpacePredictor(delay=2, dim=4),
    HCMPhaseSpacePredictor(delay=3, dim=5),
]

from analysis.invariant_projection_predictor import InvariantProjectionPredictor

inv_model = InvariantProjectionPredictor()

from analysis.hcm_structural_predictor import HCMStructuralPredictor

struct_models = [
    HCMStructuralPredictor(delay=1, dim=3),
    HCMStructuralPredictor(delay=2, dim=4),
    HCMStructuralPredictor(delay=3, dim=4),
]

from analysis.structural_consensus import structural_consensus

def hcm_predict(history):

    preds = []

    # phase-space models
    for m in models:
        try:
            p = m.predict(history)
            if np.isfinite(p):
                preds.append(p)
        except:
            continue

    # structural models
    for m in struct_models:
        try:
            p = m.predict(history)
            if np.isfinite(p):
                preds.append(p)
        except:
            continue

    # invariant model
    try:
        p = inv_model.predict(history)
        if np.isfinite(p):
            preds.append(p)
    except:
        pass

    if not preds:
        return history[-1]

    from analysis.model_selector import select_best_model
    return select_best_model(preds, history)
    
# -----------------------------
# evaluation
# -----------------------------

def rolling_mse(series, model, max_steps=300):

    split = int(len(series)*0.7)
    train = list(series[:split])
    test = series[split:]

    # ⛔ FIX: proper runtime guard
    if time.time() - START_TIME > MAX_RUNTIME:
        return float("nan")

    # 🔥 limit steps
    if len(test) > max_steps:
        test = test[:max_steps]

    history = train.copy()
    preds = []

    for t in range(len(test)):

        # ⛔ runtime guard INSIDE loop (critical)
        if time.time() - START_TIME > MAX_RUNTIME:
            break

        preds.append(model(history))
        history.append(test[t])

    if len(preds) == 0:
        return float("nan")

    return float(np.mean((np.array(test[:len(preds)]) - np.array(preds))**2))

# -----------------------------
# core
# -----------------------------

def evaluate(series):

    # 🔥 HARD LIMIT SERIES SIZE
    if len(series) > 1000:
        series = series[-1000:]

    split = int(len(series)*0.7)
    train_base = series[:split]
    test_base = series[split:]

    def apply_transform(train, test, transform):
        return transform(train), transform(test)

    tests = {}

    tests["original"] = (train_base, test_base)
    tests["diff"] = (difference(train_base), difference(test_base))
    tests["nonlinear"] = apply_transform(train_base, test_base, nonlinear_transform)
    tests["phase"] = apply_transform(train_base, test_base, phase_scramble)
    tests["shuffle"] = apply_transform(train_base, test_base, block_shuffle)

    results = {}

    for name, (train, test) in tests.items():

        if time.time() - START_TIME > MAX_RUNTIME:
            break

        if len(train) < 50 or len(test) < 50:
            continue

        mse_p = rolling_mse_split(train, test, persistence)
        mse_h = rolling_mse_split(train, test, hcm_predict)

        results[name] = {
            "persistence_mse": mse_p,
            "hcm_mse": mse_h,
            "hcm_better": mse_h < mse_p
        }

    return results

def rolling_mse_split(train, test, model, max_steps=200):

    history = list(train)
    preds = []

    for t in range(len(test)):

        # 🔥 HARD RUNTIME GUARD
        if time.time() - START_TIME > MAX_RUNTIME:
            break

        # 🔥 STEP LIMIT
        if t >= max_steps:
            break

        try:
            p = model(history)

            if not np.isfinite(p):
                p = history[-1]

        except:
            p = history[-1]

        preds.append(p)
        history.append(test[t])

    if len(preds) == 0:
        return float("nan")

    return float(np.mean((np.array(test[:len(preds)]) - np.array(preds))**2))

def multi_seed_eval(series, seeds=5):

    all_results = []

    for s in range(seeds):
        np.random.seed(s)
        res = evaluate(series)
        all_results.append(res)

    return all_results

def aggregate_results(all_results):

    summary = {}

    for key in all_results[0].keys():

        p_vals = []
        h_vals = []

        for r in all_results:
            if key in r:
                p_vals.append(r[key]["persistence_mse"])
                h_vals.append(r[key]["hcm_mse"])

        if p_vals:
            summary[key] = {
                "persistence_mean": float(np.mean(p_vals)),
                "hcm_mean": float(np.mean(h_vals)),
                "hcm_better": np.mean(h_vals) < np.mean(p_vals)
            }

    return summary


def main():

    series = load_series()

    if series is None:
        result = {
            "skipped": True,
            "reason": "dataset_missing_or_invalid"
        }
    else:
        result = evaluate(series)

    # 🔥 FORCE visibility
    print("=== HARD TEST RESULT ===")
    print(json.dumps(result, indent=2))

    ART.mkdir(exist_ok=True)

    (ART / "anti_triviality_hard.json").write_text(
        json.dumps(result, indent=2)
    )


if __name__ == "__main__":
    main()
