import numpy as np

from analysis.independent_validation import (
    estimate_alpha_welch
)

from analysis.numerical_spectral_verification import (
    estimate_alpha
)

BOOTSTRAP_ITERATIONS = 128


def bootstrap_alpha(
    series,
    estimator,
    iterations=BOOTSTRAP_ITERATIONS,
    seed=42
):

    rng = np.random.default_rng(seed)

    series = np.asarray(
        series,
        dtype=np.float64
    )

    n = len(series)

    estimates = []

    for _ in range(iterations):

        idx = rng.integers(
            0,
            n,
            n
        )

        sample = series[idx]

        try:

            alpha = estimator(sample)

            if np.isfinite(alpha):
                estimates.append(alpha)

        except Exception:
            continue

    if len(estimates) < 8:
        return None

    estimates = np.asarray(estimates)

    return {
        "mean": float(np.mean(estimates)),
        "std": float(np.std(estimates)),
        "ci_low": float(np.percentile(estimates, 2.5)),
        "ci_high": float(np.percentile(estimates, 97.5)),
        "count": int(len(estimates))
    }


def dual_bootstrap(series):

    return {
        "fft": bootstrap_alpha(
            series,
            estimate_alpha
        ),
        "welch": bootstrap_alpha(
            series,
            estimate_alpha_welch
        )
    }
