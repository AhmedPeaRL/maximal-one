import json
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd

from analysis.hcm_meta_predictor import HCMMetaPredictor

START_TIME = time.time()
MAX_RUNTIME = 300

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "artifacts"

REQUIRED_VALID_SEEDS = 6
SEEDS = tuple(range(8))
MAX_SERIES_LENGTH = 1000
MAX_STEPS = 120
MIN_TRAIN = 80
MIN_TEST = 50

def load_series():
    """
    Validation gates must fail closed.

    Missing canonical data must NEVER trigger regeneration,
    synthetic replacement, or silent substitution.
    """
    path = ROOT / "real-data" / "sunspots_global_extended.csv"

    if not path.exists():
        raise RuntimeError(
            f"Canonical validation dataset missing: {path}"
        )

    df = pd.read_csv(path)

    if len(df) < MIN_TRAIN + MIN_TEST:
        raise RuntimeError(
            f"Canonical dataset too short: {len(df)} rows"
        )

    candidates = {
        str(c).strip().lower(): c
        for c in df.columns
    }

    signal_column = None

    for name in ("sunspots", "sunspot", "value"):
        if name in candidates:
            signal_column = candidates[name]
            break

    if signal_column is None:
        raise RuntimeError(
            "No canonical signal column found. "
            "Expected one of: Sunspots, sunspot, value."
        )

    series = pd.to_numeric(
        df[signal_column],
        errors="coerce"
    ).to_numpy(dtype=np.float64)

    if not np.all(np.isfinite(series)):
        raise RuntimeError(
            "Canonical validation dataset contains non-finite values."
        )

    if np.std(series) <= 1e-12:
        raise RuntimeError(
            "Canonical validation dataset is degenerate."
        )

    if len(series) > MAX_SERIES_LENGTH:
        series = series[-MAX_SERIES_LENGTH:]

    return series

def difference(series):
    x = np.asarray(series, dtype=np.float64)

    if len(x) < 2:
        raise ValueError("Series too short for differencing.")

    return np.diff(x)

def nonlinear_transform(series):
    x = np.asarray(series, dtype=np.float64)
    return np.tanh(x) + 0.1 * np.sin(x)

def phase_scramble(series, rng):
    """
    Phase-randomized surrogate.

    Fourier magnitudes are preserved while temporal phase
    structure is randomized.

    This is a null/surrogate transformation, not evidence
    for or against HCM by itself.
    """
    x = np.asarray(series, dtype=np.float64)

    if len(x) < 8:
        raise ValueError("Series too short for phase scrambling.")

    spectrum = np.fft.rfft(x)
    amplitudes = np.abs(spectrum)

    phases = np.zeros_like(amplitudes)

    if len(phases) > 2:
        phases[1:-1] = rng.uniform(
            -np.pi,
            np.pi,
            size=len(phases) - 2
        )

    if len(x) % 2 == 0:
        phases[-1] = 0.0

    scrambled = amplitudes * np.exp(1j * phases)

    result = np.fft.irfft(
        scrambled,
        n=len(x)
    )

    return np.asarray(result, dtype=np.float64)

def block_shuffle(series, rng, block_size=20):
    x = np.asarray(series, dtype=np.float64)

    if len(x) < block_size:
        raise ValueError("Series too short for block shuffle.")

    blocks = [
        x[i:i + block_size].copy()
        for i in range(0, len(x), block_size)
    ]

    rng.shuffle(blocks)

    return np.concatenate(blocks)


def persistence(history):
    if not history:
        raise ValueError("Empty history.")

    return float(history[-1])

def rolling_mse_split(train, test, model, max_steps=MAX_STEPS):
    """
    Honest rolling evaluation.

    Model failure is recorded as failure.
    It is NEVER replaced by persistence.
    """
    history = list(np.asarray(train, dtype=np.float64))
    test = np.asarray(test, dtype=np.float64)

    if len(history) < MIN_TRAIN:
        return {
            "valid": False,
            "reason": "training_too_short"
        }

    predictions = []
    failures = []

    steps = min(len(test), max_steps)

    for t in range(steps):
        if time.time() - START_TIME > MAX_RUNTIME:
            return {
                "valid": False,
                "reason": "runtime_timeout",
                "completed_steps": t
            }

        try:
            prediction = float(model(history))

            if not np.isfinite(prediction):
                raise ValueError("non_finite_prediction")

            predictions.append(prediction)

        except Exception as exc:
            failures.append({
                "step": int(t),
                "error": type(exc).__name__,
                "message": str(exc)
            })

        history.append(float(test[t]))

    if failures:
        return {
            "valid": False,
            "reason": "model_failure",
            "completed_steps": int(steps),
            "failures": failures[:5]
        }

    if len(predictions) < 10:
        return {
            "valid": False,
            "reason": "insufficient_predictions",
            "completed_steps": int(len(predictions))
        }

    y = test[:len(predictions)]
    p = np.asarray(predictions, dtype=np.float64)

    mse = float(np.mean((y - p) ** 2))

    if not np.isfinite(mse):
        return {
            "valid": False,
            "reason": "non_finite_mse"
        }

    return {
        "valid": True,
        "mse": mse,
        "predictions": predictions,
        "n_predictions": int(len(predictions))
    }

def transform_full_series(series, name, rng):
    """
    Transform the complete series FIRST, then split.

    This prevents independently scrambling train/test and
    preserves a well-defined transformed temporal process.
    """
    if name == "original":
        return np.asarray(series, dtype=np.float64)

    if name == "diff":
        return difference(series)

    if name == "nonlinear":
        return nonlinear_transform(series)

    if name == "phase":
        return phase_scramble(series, rng)

    if name == "shuffle":
        return block_shuffle(series, rng)

    raise ValueError(f"Unknown transformation: {name}")

def evaluate_one(series, seed):
    rng = np.random.default_rng(seed)

    names = (
        "original",
        "diff",
        "nonlinear",
        "phase",
        "shuffle",
    )

    results = {}

    for name in names:

        if time.time() - START_TIME > MAX_RUNTIME:
            return {
                "valid": False,
                "reason": "runtime_timeout",
                "results": results
            }

        transformed = transform_full_series(
            series,
            name,
            rng
        )

        if len(transformed) < MIN_TRAIN + MIN_TEST:
            results[name] = {
                "valid": False,
                "reason": "transformed_series_too_short"
            }
            continue

        split = int(len(transformed) * 0.70)

        train = transformed[:split]
        test = transformed[split:]

        if len(train) < MIN_TRAIN or len(test) < MIN_TEST:
            results[name] = {
                "valid": False,
                "reason": "invalid_train_test_split"
            }
            continue

        if np.std(train) <= 1e-12 or np.std(test) <= 1e-12:
            results[name] = {
                "valid": False,
                "reason": "degenerate_signal"
            }
            continue

        hcm_model = HCMMetaPredictor()

        persistence_result = rolling_mse_split(
            train,
            test,
            persistence
        )

        hcm_result = rolling_mse_split(
            train,
            test,
            hcm_model.predict
        )

        if not persistence_result["valid"]:
            results[name] = {
                "valid": False,
                "reason": "persistence_evaluation_failed",
                "persistence": persistence_result
            }
            continue

        if not hcm_result["valid"]:
            results[name] = {
                "valid": False,
                "reason": "hcm_evaluation_failed",
                "hcm": hcm_result
            }
            continue

        p = persistence_result["mse"]
        h = hcm_result["mse"]

        results[name] = {
            "valid": True,
            "persistence_mse": p,
            "hcm_mse": h,
            "delta": float(p - h),
            "relative_gain": float(
                (p - h) / max(abs(p), 1e-12)
            ),
            "hcm_better": bool(h < p),
            "n_predictions": hcm_result["n_predictions"]
        }

    return {
        "valid": True,
        "seed": int(seed),
        "results": results
    }

def aggregate_results(runs):
    summary = {}

    names = (
        "original",
        "diff",
        "nonlinear",
        "phase",
        "shuffle",
    )

    for name in names:

        valid = []

        for run in runs:
            if not run.get("valid", False):
                continue

            value = run.get("results", {}).get(name)

            if not isinstance(value, dict):
                continue

            if not value.get("valid", False):
                continue

            if not np.isfinite(value["persistence_mse"]):
                continue

            if not np.isfinite(value["hcm_mse"]):
                continue

            valid.append(value)

        valid_count = len(valid)

        if valid_count == 0:
            summary[name] = {
                "status": "not_evaluable",
                "valid_seeds": 0,
                "required_valid_seeds": REQUIRED_VALID_SEEDS
            }
            continue

        deltas = np.asarray(
            [v["delta"] for v in valid],
            dtype=np.float64
        )

        relative_gains = np.asarray(
            [v["relative_gain"] for v in valid],
            dtype=np.float64
        )

        better = np.asarray(
            [v["hcm_better"] for v in valid],
            dtype=bool
        )

        summary[name] = {
            "status": (
                "evaluated"
                if valid_count >= REQUIRED_VALID_SEEDS
                else "insufficient_replicates"
            ),
            "valid_seeds": int(valid_count),
            "required_valid_seeds": int(REQUIRED_VALID_SEEDS),
            "persistence_mean": float(
                np.mean([
                    v["persistence_mse"]
                    for v in valid
                ])
            ),
            "hcm_mean": float(
                np.mean([
                    v["hcm_mse"]
                    for v in valid
                ])
            ),
            "delta_mean": float(np.mean(deltas)),
            "delta_median": float(np.median(deltas)),
            "relative_gain_mean": float(
                np.mean(relative_gains)
            ),
            "hcm_better_fraction": float(
                np.mean(better)
            ),
            "hcm_better_count": int(np.sum(better))
        }

    evaluable = [
        v for v in summary.values()
        if v.get("status") == "evaluated"
    ]

    return {
        "protocol": {
            "role": "anti_triviality_prediction_integrity",
            "scientific_claim": False,
            "seed_count": len(SEEDS),
            "required_valid_seeds": REQUIRED_VALID_SEEDS,
            "max_steps": MAX_STEPS,
            "transform_before_split": True,
            "model_failure_policy": "fail_closed",
            "fallback_to_persistence": False,
            "auto_dataset_regeneration": False
        },
        "summary": summary,
        "evaluable_transform_count": len(evaluable),
        "status": (
            "evaluated"
            if len(evaluable) == 5
            else "not_evaluable"
        )
    }

def to_json_safe(obj):
    if isinstance(obj, dict):
        return {
            str(k): to_json_safe(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [to_json_safe(v) for v in obj]

    if isinstance(obj, tuple):
        return [to_json_safe(v) for v in obj]

    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)

    if isinstance(obj, (np.integer, int)):
        return int(obj)

    if isinstance(obj, (np.floating, float)):
        value = float(obj)
        return value if np.isfinite(value) else None

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    return obj

def main():
    ART.mkdir(exist_ok=True)

    try:
        series = load_series()

        runs = [
            evaluate_one(series, seed)
            for seed in SEEDS
        ]

        result = aggregate_results(runs)

    except Exception as exc:
        result = {
            "protocol": {
                "role": "anti_triviality_prediction_integrity",
                "scientific_claim": False
            },
            "status": "not_evaluable",
            "error": type(exc).__name__,
            "message": str(exc)
        }

    safe = to_json_safe(result)

    print("=== ANTI-TRIVIALITY HARD TEST ===")
    print(json.dumps(safe, indent=2))

    output = ART / "anti_triviality_hard.json"
    output.write_text(
        json.dumps(safe, indent=2),
        encoding="utf-8"
    )

    if safe.get("status") != "evaluated":
        print("⚠️ ANTI-TRIVIALITY: NOT EVALUABLE")
        sys.exit(2)

    print("✅ ANTI-TRIVIALITY: EVALUATED")
    sys.exit(0)

if __name__ == "__main__":
    main()
