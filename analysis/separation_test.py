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

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    mean_null = np.mean(null_alphas)

    std_null = np.std(null_alphas) + 1e-12

    median_null = np.median(null_alphas)

    robust_std = (
        1.4826 *
        np.median(
            np.abs(
                null_alphas
                - median_null
            )
        )
        + 1e-12
    )
    
    z = abs(
        real_alpha - median_null
    ) / robust_std

    gap = abs(
        real_alpha - median_null
    )

    relative_gap = gap / (
        abs(median_null) + 1e-12
    )

    return {
        "real_alpha": float(real_alpha),
        "null_mean": float(mean_null),
        "null_median": float(median_null),
        "z_score": float(z),
        "gap": float(gap),
        "relative_gap": float(relative_gap),
        "robust_std": float(robust_std)
    }
