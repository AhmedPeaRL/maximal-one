import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha


def monte_carlo_p_value(series, observed_alpha, rng, trials=200):
    null_alphas = []

    n = len(series)

    for _ in range(trials):
        wn = rng.randn(n)
        null_alphas.append(estimate_alpha(wn))

    null_alphas = np.array(null_alphas)
    
    # pink noise (1/f)
    pink = np.cumsum(np.random.randn(n))
    pink_alpha = estimate_alpha(pink)

    p_value = np.mean(np.abs(null_alphas - np.mean(null_alphas)) >= abs(observed_alpha - np.mean(null_alphas)))
    stats = monte_carlo_p_value(series, alpha, rng)
    
    return {
        "observed_alpha": float(observed_alpha),
        "null_mean": float(np.mean(null_alphas)),
        "null_std": float(np.std(null_alphas)),
        "p_value": float(p_value)
    }
