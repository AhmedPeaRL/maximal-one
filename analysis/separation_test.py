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

    if len(series) < 64:
        return np.asarray(
            [],
            dtype=np.float64,
        )

    nperseg = min(
        256,
        len(series) // 2,
    )

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

    if total <= 0:
        return np.asarray(
            [],
            dtype=np.float64,
        )

    return (
        psd / total
    ).astype(
        np.float64
    )

def fingerprint_distance(a, b):
    m = min(
        len(a),
        len(b),
    )

    if m == 0:
        return np.nan

    a = a[:m]
    b = b[:m]

    return float(
        np.sqrt(
            np.mean(
                (a - b) ** 2
            )
        )
    )

def separation_score(
    real,
    null_samples,
):
    real_alpha = estimate_alpha(real)

    if not np.isfinite(real_alpha):
        return None

    real_fp = spectral_fingerprint(real)

    null_alphas = []
    fp_distances = []

    for sample in null_samples:
        alpha = estimate_alpha(sample)

        if not np.isfinite(alpha):
            continue

        null_alphas.append(
            float(alpha)
        )

        fp = spectral_fingerprint(sample)

        distance = fingerprint_distance(
            real_fp,
            fp,
        )

        if np.isfinite(distance):
            fp_distances.append(
                distance
            )

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
        np.percentile(
            null_alphas,
            25,
        )
    )

    q3 = float(
        np.percentile(
            null_alphas,
            75,
        )
    )

    mad = float(
        np.median(
            np.abs(
                null_alphas
                -
                median_null
            )
        )
    )

    robust_sigma = (
        1.4826 * mad
    ) + 1e-12

    gap = abs(
        real_alpha
        -
        median_null
    )

    z_score = (
        gap
        /
        robust_sigma
    )

    percentile_rank = float(
        np.mean(
            null_alphas
            <=
            real_alpha
        )
    )

    overlap_score = float(
        np.mean(
            np.abs(
                null_alphas
                -
                real_alpha
            )
            <
            robust_sigma
        )
    )

    relative_gap = (
        gap
        /
        (
            abs(median_null)
            +
            1e-12
        )
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

    return {
        "real_alpha": float(
            real_alpha
        ),
        "null_median": float(
            median_null
        ),
        "null_q1": q1,
        "null_q3": q3,
        "robust_sigma": float(
            robust_sigma
        ),
        "gap": float(gap),
        "alpha_z_score": float(
            z_score
        ),
        "relative_gap": float(
            relative_gap
        ),
        "percentile_rank": float(
            percentile_rank
        ),
        "overlap_score": float(
            overlap_score
        ),
        "fingerprint_distance_mean": (
            float(
                np.mean(fp_distances)
            )
            if len(fp_distances)
            else np.nan
        ),
        "wasserstein_distance": (
            distribution_distance
        ),
        "null_count": int(
            len(null_alphas)
        ),
    }
