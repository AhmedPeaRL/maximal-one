import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha


def monte_carlo_p_value(series, observed_alpha, trials=200):
    null_alphas = []

    n = len(series)

    for _ in range(trials):
        wn = np.random.randn(n)
        null_alphas.append(estimate_alpha(wn))

    null_alphas = np.array(null_alphas)

    p_value = np.mean(null_alphas >= observed_alpha)

    return {
        "observed_alpha": float(observed_alpha),
        "null_mean": float(np.mean(null_alphas)),
        "null_std": float(np.std(null_alphas)),
        "p_value": float(p_value)
    }
