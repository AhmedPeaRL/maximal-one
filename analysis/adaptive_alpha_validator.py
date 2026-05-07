import numpy as np


def adaptive_alpha_pass(alpha_train, alpha_test, sigma):
    """
    Adaptive validation instead of rigid threshold
    """

    if not np.isfinite(alpha_train) or not np.isfinite(alpha_test):
        return {
            "drift": np.nan,
            "tolerance": np.nan,
            "relative": np.nan,
            "pass": False,
            "reason": "non_finite_alpha"
        }

    drift = abs(alpha_train - alpha_test)

    # dynamic tolerance based on uncertainty
    tolerance = max(0.15, 2.5 * abs(sigma))

    # relative tolerance (scale-aware)
    relative = drift / (abs(alpha_train) + 1e-8)

    passed = (
        drift <= tolerance
        and relative <= 0.35
    )

    return {
        "drift": float(drift),
        "tolerance": float(tolerance),
        "relative": float(relative),
        "pass": bool(passed),
        "reason": "adaptive_pass" if passed else "adaptive_fail"
    }


def validate_single_path(result):
    required_keys = [
        "reality",
        "field",
        "envelope",
        "decision",
        "external",
        "correction",
        "timestamp"
    ]

    missing = [k for k in required_keys if k not in result]

    return {
        "valid": len(missing) == 0,
        "missing": missing
    }
