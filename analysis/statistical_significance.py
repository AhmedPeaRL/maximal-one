from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.strong_null_model import generate_strong_null

def monte_carlo_p_value(
    series,
    observed_alpha,
    rng,
    trials=50000,
):
    """
    Conservative Monte Carlo upper-tail test.

    The +1 correction prevents reporting p=0 from finite
    Monte Carlo sampling.

    IMPORTANT:
    This test does not establish a causal or physical mechanism.
    It only evaluates whether the observed alpha is unusual
    under the specified null ensemble.
    """

    n = len(series)
    null_alphas = []

    for _ in range(trials):
        sample = generate_strong_null(
            n,
            rng
        )
        if len(sample) < 256:
            sample = np.pad(
                sample,
                (0, 256 - len(sample)),
                mode="reflect"
            )

        alpha = estimate_alpha(sample)
        if np.isfinite(alpha):
            null_alphas.append(
                float(alpha)
            )
            
    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    if len(null_alphas) < 100:
        return {
            "observed_alpha": float(observed_alpha),
            "null_mean": np.nan,
            "null_std": np.nan,
            "null_median": np.nan,
            "observed_gap": np.nan,
            "exceedances": None,
            "p_value": 1.0,
            "p_value_upper_bound": 1.0,
            "null_samples": int(len(null_alphas)),
            "filtered_fraction": float(
                len(null_alphas) / max(trials, 1)
            ),
            "valid": False,
            "reason": "insufficient_null_samples",
        }

    exceedances = int(
        np.sum(
            null_alphas >= observed_alpha
        )
    )

    m = len(null_alphas)

    # Conservative finite-sample Monte Carlo estimate.
    p_value = float(
        (exceedances + 1.0)
        /
        (m + 1.0)
    )

    # Simple conservative upper confidence bound
    # using a normal approximation only as a diagnostic.
    se = np.sqrt(
        max(
            p_value * (1.0 - p_value),
            1e-12
        )
        /
        (m + 1.0)
    )

    p_upper = float(
        min(
            1.0,
            p_value + 1.96 * se
        )
    )

    return {
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
        "null_samples": int(
            m
        ),
        "filtered_fraction": float(
            m / max(trials, 1)
        ),
        "valid": True,
        "reason": None,
    }
