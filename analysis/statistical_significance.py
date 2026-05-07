import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha


def monte_carlo_p_value(series, observed_alpha, rng, trials=500):
    null_alphas = []

    n = len(series)

    for _ in range(trials):
        wn = rng.randn(n)
        alpha = estimate_alpha(wn)

        if np.isfinite(alpha):
            null_alphas.append(alpha)

    null_alphas = np.array(null_alphas)

    if len(null_alphas) < 20:
        return {
            "observed_alpha": float(observed_alpha),
            "null_mean": np.nan,
            "null_std": np.nan,
            "p_value": 1.0
        }

    p_value = max(
        1e-6,
        float(np.mean(null_alphas >= observed_alpha))
    )

    return {
        "observed_alpha": float(observed_alpha),
        "null_mean": float(np.mean(null_alphas)),
        "null_std": float(np.std(null_alphas)),
        "p_value": float(p_value),
        "null_samples": int(len(null_alphas))
    }
