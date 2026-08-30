from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)
from analysis.strong_null_model import (
    phase_surrogate_null,
)

def monte_carlo_p_value(
    series,
    observed_alpha,
    rng,
    trials=5000,
):
    """
    One-sided Monte Carlo test against phase-randomized
    surrogates of the OBSERVED series.

    Null hypothesis:
        The observed series' spectral magnitude is compatible
        with randomized Fourier phases.

    This is a spectral-surrogate test.

    It does NOT establish:
        - causality
        - consciousness
        - a physical field
        - HCM correctness

    It only tests whether the observed alpha is unusual
    under this explicitly defined surrogate construction.
    """

    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if len(series) < 256:
        return {
            "valid": False,
            "reason": "series_too_short",
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": 0,
            "exceedances": None,
            "observed_alpha": float(observed_alpha),
        }

    if not np.all(np.isfinite(series)):
        return {
            "valid": False,
            "reason": "non_finite_series",
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": 0,
            "exceedances": None,
            "observed_alpha": float(observed_alpha),
        }

    null_alphas = []

    for _ in range(trials):
        surrogate = phase_surrogate_null(
            series,
            rng,
        )

        alpha = estimate_alpha(
            surrogate
        )

        if np.isfinite(alpha):
            null_alphas.append(
                float(alpha)
            )

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64,
    )

    m = len(null_alphas)

    if m < max(
        100,
        int(0.80 * trials),
    ):
        return {
            "valid": False,
            "reason": "insufficient_valid_surrogates",
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": int(m),
            "exceedances": None,
            "observed_alpha": float(observed_alpha),
            "filtered_fraction": float(
                m / max(trials, 1)
            ),
        }

    exceedances = int(
        np.sum(
            null_alphas >= observed_alpha
        )
    )

    p_value = float(
        (exceedances + 1.0)
        /
        (m + 1.0)
    )

    se = np.sqrt(
        max(
            p_value * (1.0 - p_value),
            1e-12,
        )
        /
        (m + 1.0)
    )

    p_upper = float(
        min(
            1.0,
            p_value + 1.96 * se,
        )
    )

    return {
        "valid": True,
        "reason": None,
        "observed_alpha": float(
            observed_alpha
        ),
        "null_mean": float(
            np.mean(null_alphas)
        ),
        "null_std": float(
            np.std(null_alphas)
        ),
        "null_median": float(
            np.median(null_alphas)
        ),
        "observed_gap": float(
            observed_alpha
            -
            np.median(null_alphas)
        ),
        "exceedances": int(
            exceedances
        ),
        "p_value": float(
            p_value
        ),
        "p_value_upper_bound": float(
            p_upper
        ),
        "null_samples": int(m),
        "filtered_fraction": float(
            m / max(trials, 1)
        ),
        "null_model": (
            "phase_randomized_observed_series"
        ),
    }
