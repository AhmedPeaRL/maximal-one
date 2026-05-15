import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def separation_score(real, null_samples):

    real_alpha = estimate_alpha(real)

    null_alphas = [
        estimate_alpha(x)
        for x in null_samples
        if np.isfinite(estimate_alpha(x))
    ]

    if len(null_alphas) < 10:
        return None

    gap = real_alpha - np.mean(null_alphas)

    return {
        "real_alpha": real_alpha,
        "null_mean": float(np.mean(null_alphas)),
        "gap": float(gap),
        "std_null": float(np.std(null_alphas))
    }
