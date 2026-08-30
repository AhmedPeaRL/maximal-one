from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)
from analysis.strong_null_model import (
    permutation_null,
)

def monte_carlo_p_value(
    series,
    observed_alpha,
    rng,
    trials=5000,
):
    """
    One-sided Monte Carlo test against permutation nulls.

    Primary null hypothesis:

        The temporal ordering of the observed values does not
        provide spectral persistence beyond what is expected
        under exchangeability.

    The permutation null preserves the observed marginal
    distribution while destroying temporal ordering.

    This test does NOT establish:
        - causality
        - consciousness
        - a physical field
        - HCM correctness

    It tests only the specified spectral-persistence hypothesis
    under the permutation null.
    """

    series = np.asarray(
        series,
        dtype=np.float64,
    )

    observed_alpha = float(
        observed_alpha
    )

    if len(series) < 256:
        return {
            "valid": False,
            "reason": "series_too_short",
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": 0,
            "exceedances": None,
            "observed_alpha": observed_alpha,
            "null_model": "permutation",
        }

    if not np.all(np.isfinite(series)):
        return {
            "valid": False,
            "reason": "non_finite_series",
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": 0,
            "exceedances": None,
            "observed_alpha": observed_alpha,
            "null_model": "permutation",
        }

    if not np.isfinite(observed_alpha):
        return {
            "valid": False,
            "reason": "invalid_observed_alpha",
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": 0,
            "exceedances": None,
            "observed_alpha": observed_alpha,
            "null_model": "permutation",
        }

    null_alphas = []

    for _ in range(
        int(trials)
    ):
        surrogate = permutation_null(
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

    minimum_valid = max(
        100,
        int(0.80 * trials),
    )

    if m < minimum_valid:
        return {
            "valid": False,
            "reason": "insufficient_valid_surrogates",
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": int(m),
            "exceedances": None,
            "observed_alpha": observed_alpha,
            "filtered_fraction": float(
                m / max(trials, 1)
            ),
            "null_model": "permutation",
        }

    exceedances = int(
        np.sum(
            null_alphas >= observed_alpha
        )
    )

    # +1 correction prevents an artificial p=0.
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
        "observed_alpha": observed_alpha,
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
        "p_value": p_value,
        "p_value_upper_bound": p_upper,
        "null_samples": int(m),
        "filtered_fraction": float(
            m / max(trials, 1)
        ),
        "null_model": "permutation",
    }
