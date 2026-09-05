from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)

SEEDS = (
    11,
    42,
    101,
    777,
    2025,
)

PERTURBATION_FRACTION = 0.05
MAX_STD_ALPHA = 0.10

def run(series):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        return {
            "valid": False,
            "reason": "series_not_1d",
            "seed_stable": False,
        }

    if not np.all(np.isfinite(series)):
        return {
            "valid": False,
            "reason": "non_finite_series",
            "seed_stable": False,
        }

    base_std = float(np.std(series))

    if base_std < 1e-12:
        return {
            "valid": False,
            "reason": "degenerate_series",
            "seed_stable": False,
        }

    records = []

    for seed in SEEDS:

        rng = np.random.default_rng(seed)

        perturbation = rng.normal(
            loc=0.0,
            scale=base_std * PERTURBATION_FRACTION,
            size=len(series),
        )

        test_series = (
            series +
            perturbation
        )

        alpha = estimate_alpha(
            test_series
        )

        if np.isfinite(alpha):
            records.append(
                {
                    "seed": int(seed),
                    "alpha": float(alpha),
                }
            )

    if len(records) < 3:
        return {
            "valid": False,
            "reason": "insufficient_valid_seeds",
            "seed_stable": False,
            "records": records,
        }

    alphas = np.asarray(
        [r["alpha"] for r in records],
        dtype=np.float64,
    )

    mean_alpha = float(
        np.mean(alphas)
    )

    std_alpha = float(
        np.std(alphas)
    )

    return {
        "valid": True,

        # Explicitly name what this test actually measures.
        "test_type": "perturbation_stability",

        "records": records,

        "mean_alpha": mean_alpha,
        "std_alpha": std_alpha,

        "max_allowed_std": MAX_STD_ALPHA,

        "seed_stable": bool(
            std_alpha < MAX_STD_ALPHA
        ),
    }
