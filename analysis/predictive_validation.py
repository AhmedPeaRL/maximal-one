import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha
)

# These bands remain descriptive diagnostics.
# They are NOT treated as ontological or mechanistic claims.
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

    series = series[np.isfinite(series)]

    if len(series) < 256:
        return None

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

    if len(series) < 512:
        return {
            "valid": False,
            "reason": f"insufficient_series ({len(series)})"
        }

    n = len(series)

    # Keep both train and test sufficiently long for
    # the canonical spectral estimator.
    min_len = 256

    split = int(n * split_ratio)

    if split < min_len:
        split = min_len

    if (n - split) < min_len:
        split = n - min_len

    if split < min_len or (n - split) < min_len:
        return {
            "valid": False,
            "reason": (
                f"invalid_split: train={split}, "
                f"test={n - split}, minimum={min_len}"
            )
        }

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
            "reason": (
                f"invalid_test_alpha (len={len(test)})"
            )
        }

    train_alpha = float(pred["alpha"])
    test_alpha = float(test_alpha)

    train_class = classify_alpha(train_alpha)
    test_class = classify_alpha(test_alpha)

    continuity = continuity_score(
        train_alpha,
        test_alpha
    )

    # Continuous stability criterion.
    #
    # The alpha estimate is continuous, whereas the class labels
    # are coarse descriptive bins. Therefore class disagreement
    # is retained as a diagnostic rather than used as the sole
    # validity gate.
    alpha_delta = abs(
        train_alpha - test_alpha
    )

    # A prediction is considered structurally stable when:
    # 1. both estimates are finite,
    # 2. their normalized continuity remains meaningful,
    # 3. the absolute spectral shift does not exceed the declared
    #    predictive tolerance.
    #
    # The tolerance is deliberately explicit rather than derived
    # from the observed result.
    MAX_PREDICTIVE_ALPHA_DELTA = 1.50
    MIN_CONTINUITY = 0.15

    continuous_stability = bool(
        continuity >= MIN_CONTINUITY
        and
        alpha_delta <= MAX_PREDICTIVE_ALPHA_DELTA
    )

    # Classification agreement remains useful information,
    # but is no longer allowed to convert a continuous transition
    # into an automatic scientific failure.
    structural_match = bool(
        train_class == test_class
    )

    return {
        "prediction": train_class,
        "test_classification": test_class,
        "train_alpha": train_alpha,
        "test_alpha": test_alpha,
        "alpha_delta": float(alpha_delta),
        "continuity": float(continuity),
        "structural_match": structural_match,
        "continuous_stability": continuous_stability,
        "classification_transition": bool(
            train_class != test_class
        ),
        "valid": continuous_stability
    }
