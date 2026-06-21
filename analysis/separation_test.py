import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def separation_score(real, null_samples):
    real_alpha = estimate_alpha(real)
    null_alphas = []

    for s in null_samples:
        a = estimate_alpha(s)

        if np.isfinite(a):
            null_alphas.append(a)

    if len(null_alphas) < 20:
        return None

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    median_null = np.median(null_alphas)

    q1 = np.percentile(null_alphas, 25)
    q3 = np.percentile(null_alphas, 75)

    iqr = q3 - q1 + 1e-12
    robust_sigma = iqr / 1.349

    gap = abs(
        real_alpha
        -
        np.mean(null_alphas)
    )

    effect_size = gap / (
        np.std(null_alphas) + 1e-12
    )

    z_score = gap / (
        robust_sigma + 1e-12
    )

    relative_gap = gap / (
        abs(median_null)
        + 1e-12
    )

    percentile_rank = float(
        np.mean(
            np.abs(null_alphas - median_null)
            <
            np.abs(real_alpha - median_null)
        )
    )

    return {
        "real_alpha": float(real_alpha),
        "null_median": float(median_null),
        "null_q1": float(q1),
        "null_q3": float(q3),
        "robust_sigma": float(robust_sigma),
        "gap": float(gap),
        "effect_size": float(effect_size),
        "z_score": float(z_score),
        "relative_gap": float(relative_gap),
        "percentile_rank": percentile_rank,
        "null_count": int(
            len(null_alphas)
        )
    }
