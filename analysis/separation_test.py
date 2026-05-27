import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def separation_score(real, null_samples):
    real_alpha = estimate_alpha(real)

    null_alphas = [
        estimate_alpha(s)
        for s in null_samples
        if np.isfinite(estimate_alpha(s))
    ]

    if len(null_alphas) < 10:
        return None

    null_alphas = np.array(null_alphas)

    mean_null = np.mean(null_alphas)
    std_null = np.std(null_alphas) + 1e-12

    if std_null < 1e-3:
        return None

    z = (real_alpha - mean_null) / (std_null + 1e-12)
    z = abs(z)

    # 🔥 NEW: minimum enforced gap
    gap = abs(real_alpha - mean_null)

    return {
        "real_alpha": float(real_alpha),
        "null_mean": float(mean_null),
        "z_score": float(z),
        "gap": float(gap),
        "std_null": float(std_null)
    }
