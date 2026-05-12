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

    if len(series) < 128:
        return None

    alpha = estimate_alpha(series)

    if not np.isfinite(alpha):
        return None

    return {
        "alpha": float(alpha),
        "classification": classify_alpha(alpha)
    }


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
            "reason": "insufficient_series"
        }

    split = int(len(series) * split_ratio)

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
            "reason": "invalid_test_alpha"
        }

    drift = abs(
        pred["alpha"] - test_alpha
    )

    tolerance = max(
        0.35,
        0.35 * abs(pred["alpha"])
    )

    passed = drift <= tolerance

    return {
        "prediction": pred["classification"],
        "train_alpha": float(pred["alpha"]),
        "test_alpha": float(test_alpha),
        "drift": float(drift),
        "tolerance": float(tolerance),
        "valid": bool(passed)
}
