import numpy as np

from analysis.numerical_spectral_verification import (
    estimate_alpha
)

def classify_alpha(alpha):
    if not np.isfinite(alpha):
        return "invalid"

    if alpha >= 1.5:
        return "persistent_trend"

    if alpha >= 0.75:
        return "moderate_memory"

    return "random_like"

def predict_next_trend(series):
    series = np.asarray(
        series,
        dtype=np.float64
    )

    if len(series) < 256:
        series = np.pad(series, (0, 256-len(series)), mode='wrap')

    alpha = estimate_alpha(series)
    
    if not np.isfinite(alpha):
        return None

    return {
        "alpha": float(alpha),
        "classification": classify_alpha(alpha)
    }

def continuity_score(a, b):
    if not (
        np.isfinite(a)
        and np.isfinite(b)
    ):
        return 0.0

    denom = max(
        abs(a),
        abs(b),
        1e-9
    )

    return float(
        1.0 - min(
            1.0,
            abs(a - b) / denom
        )
    )

def evaluate_prediction(
    series,
    split_ratio=0.8
):

    series = np.asarray(
        series,
        dtype=np.float64
    )

    series = series[np.isfinite(series)]

    if len(series) < 256:
        return {
            "valid": False,
            "reason": f"insufficient_series ({len(series)})"
        }

    n = len(series)

    # 🔥 enforce minimum segment length
    min_len = 150

    split = int(n * split_ratio)

    # 🔥 adjust split to guarantee both sides valid
    if split < min_len:
        split = min_len

    if (n - split) < min_len:
        split = n - min_len

    train = series[:split]
    test = series[split:]

    pred = predict_next_trend(train)

    if pred is None:
        return {
            "valid": False,
            "reason": "prediction_failed"
        }

    test_alpha = estimate_alpha(test)

    if not np.isfinite(test_alpha):
        return {
            "valid": False,
            "reason": f"invalid_test_alpha (len={len(test)})"
        }

    train_class = pred["classification"]
    test_class = classify_alpha(test_alpha)

    continuity = continuity_score(
        pred["alpha"],
        test_alpha
    )

    structural_match = (
        train_class == test_class
    )

    valid = bool(
        continuity >= 0.15 and
        structural_match
    )

    return {
        "prediction": train_class,
        "test_classification": test_class,
        "train_alpha": float(pred["alpha"]),
        "test_alpha": float(test_alpha),
        "continuity": float(continuity),
        "structural_match": bool(structural_match),
        "valid": valid
    }
