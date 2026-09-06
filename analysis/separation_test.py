from __future__ import annotations
import numpy as np
from scipy.signal import welch
from scipy.stats import wasserstein_distance
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)

def spectral_fingerprint(series):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1 or len(series) < 64:
        return np.asarray([], dtype=np.float64)

    nperseg = min(
        256,
        len(series) // 2,
    )

    if nperseg < 16:
        return np.asarray([], dtype=np.float64)

    freqs, psd = welch(
        series,
        nperseg=nperseg,
        window="hann",
        detrend="linear",
        scaling="density",
    )

    mask = (
        np.isfinite(freqs)
        & np.isfinite(psd)
        & (freqs > 0)
        & (psd >= 0)
    )

    psd = psd[mask]

    total = np.sum(psd)

    if not np.isfinite(total) or total <= 0:
        return np.asarray([], dtype=np.float64)

    return (
        psd / total
    ).astype(np.float64)

def fingerprint_distance(a, b):
    m = min(len(a), len(b))

    if m == 0:
        return np.nan

    return float(
        np.sqrt(
            np.mean(
                (a[:m] - b[:m]) ** 2
            )
        )
    )

def separation_score(real, null_samples):
    """
    Compare the observed spectral exponent against a supplied
    null ensemble.

    IMPORTANT:
    - A robust z-score is reported only when MAD > 0.
    - A collapsed null distribution NEVER produces an artificial z-score.
    - Empirical upper-tail probability is reported separately.
    """

    real_alpha = estimate_alpha(real)

    if not np.isfinite(real_alpha):
        return None

    real_fp = spectral_fingerprint(real)

    if len(real_fp) == 0:
        return None

    null_alphas = []
    fp_distances = []

    for sample in null_samples:
        alpha = estimate_alpha(sample)

        if not np.isfinite(alpha):
            continue

        fp = spectral_fingerprint(sample)

        if len(fp) == 0:
            continue

        distance = fingerprint_distance(
            real_fp,
            fp,
        )

        null_alphas.append(float(alpha))

        if np.isfinite(distance):
            fp_distances.append(float(distance))

    if len(null_alphas) < 20:
        return None

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64,
    )

    fp_distances = np.asarray(
        fp_distances,
        dtype=np.float64,
    )

    median_null = float(
        np.median(null_alphas)
    )

    q1 = float(
        np.percentile(null_alphas, 25)
    )

    q3 = float(
        np.percentile(null_alphas, 75)
    )

    mad = float(
        np.median(
            np.abs(
                null_alphas -
                median_null
            )
        )
    )

    robust_sigma = float(
        1.4826 * mad
    )

    gap = float(
        real_alpha -
        median_null
    )

    absolute_gap = abs(gap)

    # Robust z-score is valid only for non-degenerate null scale.
    if robust_sigma > 0:
        z_score = float(
            absolute_gap /
            robust_sigma
        )
        z_valid = True
    else:
        z_score = None
        z_valid = False

    # One-sided empirical upper-tail probability.
    # +1 correction avoids reporting p=0.
    exceedances = int(
        np.sum(
            null_alphas >= real_alpha
        )
    )

    empirical_p_upper = float(
        (exceedances + 1.0) /
        (len(null_alphas) + 1.0)
    )

    percentile_rank = float(
        np.mean(
            null_alphas <= real_alpha
        )
    )

    null_degenerate = bool(
        robust_sigma <= 0
    )

    if robust_sigma > 0:
        overlap_score = float(
            np.mean(
                np.abs(
                    null_alphas -
                    real_alpha
                ) < robust_sigma
            )
        )
    else:
        # For a degenerate null, overlap means exact equality.
        overlap_score = float(
            np.mean(
                null_alphas == real_alpha
            )
        )

    relative_gap = (
        float(
            absolute_gap /
            abs(median_null)
        )
        if abs(median_null) > 0
        else None
    )

    distribution_distance = float(
        wasserstein_distance(
            null_alphas,
            np.repeat(
                real_alpha,
                len(null_alphas),
            ),
        )
    )

    z_interpretation = (
        "valid_robust_separation_against_supplied_null"    if z_valid and not null_degenerate
        else
        "z_score_not_interpretable_as_strength"
    )

    return {
        "real_alpha": float(real_alpha),
        "null_median": median_null,
        "null_q1": q1,
        "null_q3": q3,
        "robust_sigma": robust_sigma,
        "gap": absolute_gap,
        "alpha_z_score": z_score,
        "z_score_valid": bool(z_valid),
        "z_score_interpretation": z_interpretation,
        "interpretation": (
            "Observed alpha is separated from the supplied "
            "permutation-null ensemble; this does not establish "
            "mechanism, universality, or HCM causation."
        ),
        "null_degenerate": null_degenerate,
        "empirical_p_upper": empirical_p_upper,
        "null_exceedances": int(exceedances),
        "relative_gap": relative_gap,
        "percentile_rank": percentile_rank,
        "overlap_score": overlap_score,
        "fingerprint_distance_mean": (
            float(np.mean(fp_distances))
            if len(fp_distances)
            else np.nan
        ),
        "wasserstein_distance":
            distribution_distance,
        "null_count":
            int(len(null_alphas)),
    }
