import numpy as np

from analysis.numerical_spectral_verification import (
    estimate_alpha
)


def bootstrap_alpha_distribution(
    series,
    rng,
    n_boot=64,
    block_size=32
):

    series = np.asarray(
        series,
        dtype=np.float64
    )

    n = len(series)

    if n < block_size + 1:
        return {
            "mean": np.nan,
            "std": np.nan,
            "valid": 0
        }

    alphas = []

    for _ in range(n_boot):

        sample = []

        while len(sample) < n:

            max_start = max(1, n - block_size)
            start = rng.randint(0, max_start)

            block = series[
                start:start + block_size
            ]

            sample.extend(block)

        sample = np.asarray(
            sample[:n],
            dtype=np.float64
        )

        alpha = estimate_alpha(sample)

        if np.isfinite(alpha):
            alphas.append(alpha)

    alphas = np.asarray(
        alphas,
        dtype=np.float64
    )

    if len(alphas) < 8:

        return {
            "mean": np.nan,
            "std": np.nan,
            "valid": 0
        }

    return {
        "mean": float(np.mean(alphas)),
        "std": float(np.std(alphas)),
        "valid": int(len(alphas))
    }
