import numpy as np


def temporal_asymmetry(series):

    x = np.asarray(series, dtype=np.float64)

    if len(x) < 32:
        return np.nan

    dx = np.diff(x)

    if len(dx) < 8:
        return np.nan

    m3 = np.mean(dx ** 3)

    s3 = (np.std(dx) ** 3) + 1e-12

    score = m3 / s3

    return float(score)


def irreversibility_pass(real, surrogate_pool):

    real_score = temporal_asymmetry(real)

    surrogate_scores = []

    for s in surrogate_pool:

        val = temporal_asymmetry(s)

        if np.isfinite(val):
            surrogate_scores.append(val)

    surrogate_scores = np.asarray(
        surrogate_scores,
        dtype=np.float64
    )

    if len(surrogate_scores) < 8:

        return {
            "pass": False,
            "reason": "insufficient_surrogates"
        }

    mu = np.mean(surrogate_scores)

    sigma = np.std(surrogate_scores)

    z = (
        (real_score - mu)
        / (sigma + 1e-12)
    )

    passed = abs(z) > 2.0

    return {
        "real_score": float(real_score),
        "null_mean": float(mu),
        "null_std": float(sigma),
        "z_score": float(z),
        "pass": bool(passed)
    }
