import numpy as np
from scipy.signal import welch
from analysis.numerical_spectral_verification import estimate_alpha

def spectral_fingerprint(series):
    freqs, psd = welch(
        series,
        nperseg=min(256, len(series)//2)
    )

    psd = psd / (
        np.sum(psd) + 1e-12
    )

    return psd.astype(np.float64)

def fingerprint_distance(a, b):
    m = min(len(a), len(b))

    a = a[:m]
    b = b[:m]

    return float(
        np.sqrt(
            np.mean(
                (a - b) ** 2
            )
        )
    )

def separation_score(real, null_samples):
    real_alpha = estimate_alpha(real)
    real_fp = spectral_fingerprint(real)

    null_alphas = []
    fp_distances = []

    for s in null_samples:

        alpha = estimate_alpha(s)

        if np.isfinite(alpha):

            null_alphas.append(alpha)

            fp = spectral_fingerprint(s)

            fp_distances.append(
                fingerprint_distance(
                    real_fp,
                    fp
                )
            )

    if len(null_alphas) < 20:
        return None

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    fp_distances = np.asarray(
        fp_distances,
        dtype=np.float64
    )

    median_null = np.median(null_alphas)

    gap = abs(
        real_alpha
        -
        median_null
    )

    alpha_effect = gap / (
        np.std(null_alphas) + 1e-12
    )

    spectral_effect = np.mean(
        fp_distances
    )

    composite_effect = (
        0.5 * alpha_effect
        +
        0.5 * spectral_effect
    )

    return {

        "real_alpha": float(real_alpha),

        "null_median": float(
            median_null
        ),

        "alpha_effect": float(
            alpha_effect
        ),

        "spectral_effect": float(
            spectral_effect
        ),

        "effect_size": float(
            composite_effect
        ),

        "fingerprint_distance_mean":
        float(
            spectral_effect
        ),

        "null_count":
        int(
            len(null_alphas)
        )
    }
