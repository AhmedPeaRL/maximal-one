from __future__ import annotations
import numpy as np
from scipy.stats import beta
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)
from analysis.strong_null_model import (
    permutation_null,
)

def _invalid_result(
    reason,
    observed_alpha,
    null_samples=0,
    exceedances=None,
):
    return {
        "valid": False,
        "reason": reason,

        "observed_alpha": float(
            observed_alpha
        ),

        "null_model": "permutation",

        "null_hypothesis": (
            "exchangeable_values:"
            "temporal_ordering_carries_no_additional_"
            "spectral_persistence"
        ),

        "null_samples": int(
            null_samples
        ),

        "exceedances": exceedances,

        # Backward-compatible field.
        "p_value": 1.0,

        "p_value_mc_add_one": 1.0,

        "p_value_95pct_upper_exact": 1.0,
    }

def monte_carlo_p_value(
    series,
    observed_alpha,
    rng,
    trials=5000,
):
    """
    One-sided Monte Carlo test against a permutation null.

    PRIMARY INFERENCE:

        H0:
        The observed values are exchangeable with respect
        to temporal ordering, so temporal ordering carries
        no additional spectral persistence.

    The permutation preserves the observed marginal
    distribution while destroying temporal ordering.

    This procedure tests only the specified statistical null.

    It does NOT establish:

        - causality
        - consciousness
        - a physical field
        - NEF
        - HCM correctness
        - universality
    """

    series = np.asarray(
        series,
        dtype=np.float64,
    )

    try:
        observed_alpha = float(
            observed_alpha
        )
    except (
        TypeError,
        ValueError,
    ):
        return _invalid_result(
            "invalid_observed_alpha",
            np.nan,
        )

    if len(series) < 256:
        return _invalid_result(
            "series_too_short",
            observed_alpha,
        )

    if not np.all(
        np.isfinite(series)
    ):
        return _invalid_result(
            "non_finite_series",
            observed_alpha,
        )

    if not np.isfinite(
        observed_alpha
    ):
        return _invalid_result(
            "invalid_observed_alpha",
            observed_alpha,
        )

    trials = int(trials)

    if trials < 1:
        return _invalid_result(
            "invalid_trial_count",
            observed_alpha,
        )

    null_alphas = []

    for _ in range(trials):

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

    m = len(
        null_alphas
    )

    minimum_valid = max(
        100,
        int(
            0.80 * trials
        ),
    )

    if m < minimum_valid:
        return _invalid_result(
            "insufficient_valid_surrogates",
            observed_alpha,
            null_samples=m,
        ) | {
            "filtered_fraction": float(
                m / max(trials, 1)
            )
        }

    exceedances = int(
        np.sum(
            null_alphas >= observed_alpha
        )
    )

    # ------------------------------------------------------------
    # Monte Carlo +1 correction.
    #
    # This avoids the invalid statement p=0 when no sampled
    # null exceeds the observed statistic.
    # ------------------------------------------------------------

    p_mc = float(
        (exceedances + 1.0)
        /
        (m + 1.0)
    )

    # ------------------------------------------------------------
    # Exact one-sided 95% upper confidence bound for the
    # underlying exceedance probability.
    #
    # If k exceedances are observed in m valid null samples:
    #
    #     p_upper = Beta^{-1}(0.95, k+1, m-k)
    #
    # This is preferable to a normal approximation when p is
    # very small.
    # ------------------------------------------------------------

    if exceedances >= m:
        p_upper = 1.0

    else:
        p_upper = float(
            beta.ppf(
                0.95,
                exceedances + 1,
                m - exceedances,
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

        "null_samples": int(
            m
        ),

        "filtered_fraction": float(
            m / max(trials, 1)
        ),

        "null_model": "permutation",

        "null_hypothesis": (
            "exchangeable_values:"
            "temporal_ordering_carries_no_additional_"
            "spectral_persistence"
        ),

        "test_interpretation": (
            "Evidence against the specified exchangeability/"
            "permutation null only. This is not independent "
            "evidence from the separation diagnostic when "
            "the same permutation ensemble is used."
        ),

        "p_value": p_mc,

        "p_value_mc_add_one": p_mc,

        "p_value_95pct_upper_exact": p_upper,

        "multiple_testing_note": (
            "The inferential interpretation is valid only "
            "for the predeclared primary endpoint and null. "
            "Secondary diagnostics must not be treated as "
            "independent replicated tests."
        ),
    }
