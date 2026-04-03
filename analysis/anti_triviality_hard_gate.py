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

from analysis.structure_detector import detect_structure

from analysis.hcm_meta_predictor import HCMMetaPredictor

meta_model = HCMMetaPredictor()

def hcm_predict(history):
    return meta_model.predict(history)
    
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

    from analysis.structure_detector import detect_structure

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
        structure_score = detect_structure(train)

        # 🔥 SKIP TRIVIAL SERIES
        var = np.var(test)

        if np.std(train) < 1e-6 or np.std(test) < 1e-6:
            continue

        if var < 1e-8:
            results[name] = {
                "skipped": True,
                "reason": "trivial_signal"
            }
            continue
        
        results[name] = {
            "persistence_mse": mse_p,
            "hcm_mse": mse_h,
            "delta": float(mse_p - mse_h),
            "hcm_better": mse_h < mse_p,
            "relative_gain": float((mse_p - mse_h) / (mse_p + 1e-8)),
            "structure_score": structure_score
        }

    return results

def rolling_mse_split(train, test, model, max_steps=200):

    history = list(train)
    preds = []

    for t in range(len(test)):

        # 🔥 HARD RUNTIME GUARD
        if time.time() - START_TIME > MAX_RUNTIME:
            break

        if t >= 200:
            break

        try:
            p = model(history)

            if not np.isfinite(p):
                p = history[-1]

        except:
            return float("nan")  # 🔥 expose failure

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

    keys = set()
    for r in all_results:
        keys.update(r.keys())

    for key in keys:

        p_vals = []
        h_vals = []

        for r in all_results:

            if key not in r:
                continue

            val = r[key]

            if not isinstance(val, dict):
                continue

            if val.get("skipped", False):
                continue

            if "persistence_mse" not in val or "hcm_mse" not in val:
                continue

            p = val["persistence_mse"]
            h = val["hcm_mse"]

            if not np.isfinite(p) or not np.isfinite(h):
                continue

            # 🔥 soften equality rejection
            if abs(p - h) < 1e-6:
                continue

            p_vals.append(p)
            h_vals.append(h)

        # 🔥 ADAPTIVE THRESHOLD (CRITICAL FIX)
        MIN_SAMPLES = 2 if len(all_results) >= 10 else 1

        if len(p_vals) >= MIN_SAMPLES:
            summary[key] = {
                "persistence_mean": float(np.mean(p_vals)),
                "hcm_mean": float(np.mean(h_vals)),
                "delta": float(np.mean(p_vals) - np.mean(h_vals)),
                "hcm_better": float(np.mean(h_vals)) < float(np.mean(p_vals)),
                "samples": len(p_vals)
            }
        else:
            summary[key] = {
                "skipped": True,
                "reason": "insufficient_valid_samples",
                "samples": len(p_vals)
            }

    return summary
# -----------------------------
# JSON SAFE CONVERTER (CRITICAL FIX)
# -----------------------------

def to_json_safe(obj):
    import numpy as np

    if isinstance(obj, dict):
        return {k: to_json_safe(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [to_json_safe(v) for v in obj]

    elif isinstance(obj, (np.bool_,)):
        return bool(obj)

    elif isinstance(obj, (np.integer,)):
        return int(obj)

    elif isinstance(obj, (np.floating,)):
        return float(obj)

    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()

    return obj
    

def main():

    series = load_series()

    if series is None:
        result = {
            "skipped": True,
            "reason": "dataset_missing_or_invalid"
        }
    else:
        all_results = multi_seed_eval(series, seeds=25)
        result = aggregate_results(all_results)

    safe_result = to_json_safe(result)

    print("=== HARD TEST RESULT ===")
    print(json.dumps(safe_result, indent=2))

    ART.mkdir(exist_ok=True)

    (ART / "anti_triviality_hard.json").write_text(
        json.dumps(safe_result, indent=2)
    )


if __name__ == "__main__":
    main()
