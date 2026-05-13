import numpy as np


def adaptive_alpha_pass(
    alpha_train,
    alpha_test,
    alpha_sigma
):

    if (
        not np.isfinite(alpha_train)
        or not np.isfinite(alpha_test)
        or not np.isfinite(alpha_sigma)
    ):

        return {
            "drift": np.nan,
            "tolerance": np.nan,
            "relative": np.nan,
            "pass": False,
            "reason": "non_finite"
        }

    drift = abs(
        alpha_train - alpha_test
    )

    tolerance = max(
        0.25,
        2.5 * alpha_sigma
    )

    scale = max(
        abs(alpha_train),
        alpha_sigma,
        0.35
    )

    relative = drift / scale

    passed = (
        drift <= tolerance
        and relative <= max(0.75, 2.0 * alpha_sigma)
    )

    return {
        "drift": float(drift),
        "tolerance": float(tolerance),
        "relative": float(relative),
        "pass": bool(passed),
        "reason": (
            "adaptive_pass"
            if passed
            else "adaptive_fail"
        )
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
