import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha
)

SEEDS = [11,42,101,777,2025]

def run(series):
    alphas = []

    for seed in SEEDS:

        rng = np.random.default_rng(seed)

        perturbation = rng.normal(
            0,
            np.std(series) * 0.05,
            len(series)
        )

        test_series = (
            series
            +
            perturbation
        )

        alpha = estimate_alpha(
            test_series
        )

        if np.isfinite(alpha):
            alphas.append(alpha)

    if len(alphas) < 3:

        return {
            "valid": False
        }

    alphas = np.asarray(
        alphas,
        dtype=np.float64
    )

    return {
        "valid": True,
        "mean_alpha": float(
            np.mean(alphas)
        ),
        "std_alpha": float(
            np.std(alphas)
        ),
        "seed_stable": bool(
            np.std(alphas) < 0.10
        )
    }
