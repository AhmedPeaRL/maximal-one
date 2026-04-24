import numpy as np

def adaptive_alpha_pass(alpha_train, alpha_test, sigma):
    """
    Adaptive validation instead of rigid threshold
    """

    drift = abs(alpha_train - alpha_test)

    # dynamic tolerance based on uncertainty
    tolerance = 2.5 * sigma

    # relative tolerance (scale-aware)
    relative = drift / (abs(alpha_train) + 1e-8)

    return {
        "drift": drift,
        "tolerance": tolerance,
        "relative": relative,
        "pass": drift < tolerance or relative < 0.25
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
