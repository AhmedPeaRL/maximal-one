import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def separation_score(real, null_samples):
    real_alpha = estimate_alpha(real)

def null_model(n, rng):
    x = rng.standard_normal(n)
    x = np.cumsum(x)
    return x

    if len(null_alphas) < 10:
        return None

    gap = (real_alpha - np.mean(null_alphas)) / (np.std(null_alphas) + 1e-12)

    return {
        "real_alpha": real_alpha,
        "null_mean": float(np.mean(null_alphas)),
        "gap": float(gap),
        "std_null": float(np.std(null_alphas))
    }
