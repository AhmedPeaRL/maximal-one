import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def separation_score(real, null_samples):
    real_alpha = estimate_alpha(real)

    null_alphas = []

    for s in null_samples:
        a = estimate_alpha(s)
        if np.isfinite(a):
            null_alphas.append(a)

    if len(null_alphas) < 10:
        return None

    null_alphas = np.array(null_alphas)
  
    gap = abs(real_alpha - np.mean(null_alphas)) / (np.std(null_alphas) + 1e-6)

    if gap < 1.2:
        return {
            "real_alpha": float(real_alpha),
            "null_mean": float(np.mean(null_alphas)),
            "gap": float(gap),
            "std_null": float(np.std(null_alphas)),
            "warning": "weak separation"
        }
    
    return {
        "real_alpha": float(real_alpha),
        "null_mean": float(np.mean(null_alphas)),
        "gap": float(gap),
        "std_null": float(np.std(null_alphas))
    }
