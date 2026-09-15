from __future__ import annotations
import numpy as np
from scipy.signal import welch
from scipy.stats import wasserstein_distance
from analysis.numerical_spectral_verification import (
    CANONICAL_DETREND,
    CANONICAL_NPERSEG,
    CANONICAL_SCALING,
    CANONICAL_WINDOW,
    estimate_alpha,
)

def spectral_fingerprint(series):
    """
    Construct a normalized spectral fingerprint using the
    canonical Welch segmentation configuration.

    IMPORTANT:

    This fingerprint is a secondary diagnostic representation.

    It is not an independent inferential test.

    The canonical alpha endpoint remains defined by
    estimate_alpha(), not by fingerprint distance.
    """

    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        return np.asarray([], dtype=np.float64)

    if len(series) < 64:
        return np.asarray([], dtype=np.float64)

    nperseg = min(
        CANONICAL_NPERSEG,
        len(series),
    )

    if nperseg < 128:
        return np.asarray([], dtype=np.float64)

    try:
        freqs, psd = welch(
            series,
            nperseg=nperseg,
            window=CANONICAL_WINDOW,
            detrend=CANONICAL_DETREND,
            scaling=CANONICAL_SCALING,
        )
    except Exception:
        return np.asarray([], dtype=np.float64)

    mask = (
        np.isfinite(freqs)
        & np.isfinite(psd)
        & (freqs > 0)
        & (psd >= 0)
    )

    psd = psd[mask]

    if len(psd) == 0:
        return np.asarray([], dtype=np.float64)

    total = np.sum(psd)

    if not np.isfinite(total) or total <= 0:
        return np.asarray([], dtype=np.float64)

    return (
        psd / total
    ).astype(np.float64)

def fingerprint_distance(a, b):
    """
    Root-mean-square distance between two spectral fingerprints.

    This is descriptive only.
    """

    m = min(
        len(a),
        len(b),
    )

    if m == 0:
        return np.nan

    return float(
        np.sqrt(
            np.mean(
                (
                    a[:m]
                    -
                    b[:m]
                ) ** 2
            )
        )
    )

def separation_score(
    real,
    null_samples,
):
    """
    Secondary separation diagnostic.

    Scientific interpretation:

    - The canonical alpha endpoint is recomputed with
      estimate_alpha().
    - The supplied null ensemble is evaluated without
      pretending it is an independent replication.
    - Robust separation statistics are reported descriptively.
    - The permutation null used here must not be described
      as independent evidence when the primary statistical
      test uses the same null family.
    - Fingerprint distance is descriptive only.
    - No mechanism, universality, consciousness, NEF,
      HCM causation, or independent replication is inferred.

    This function intentionally does NOT create a new
    scientific claim-support basis.
    """

    real_alpha = estimate_alpha(
        real
    )

    if not np.isfinite(real_alpha):
        return None

    real_fp = spectral_fingerprint(
        real
    )

    if len(real_fp) == 0:
        return None

    null_alphas = []
    fp_distances = []

    for sample in null_samples:
        alpha = estimate_alpha(
            sample
        )

        if not np.isfinite(alpha):
            continue

        fp = spectral_fingerprint(
            sample
        )

        if len(fp) == 0:
            continue

        distance = fingerprint_distance(
            real_fp,
            fp,
        )

        null_alphas.append(
            float(alpha)
        )

        if np.isfinite(distance):
            fp_distances.append(
                float(distance)
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
        np.median(
            null_alphas
        )
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

    robust_sigma = float(
        1.4826 * mad
    )

    gap = float(
        real_alpha
        -
        median_null
    )

    absolute_gap = abs(
        gap
    )

    if robust_sigma > 0:
        z_score = float(
            absolute_gap
            /
            robust_sigma
        )

        z_valid = True

    else:
        z_score = None
        z_valid = False

    exceedances = int(
        np.sum(
            null_alphas >= real_alpha
        )
    )

    empirical_p_upper = float(
        (
            exceedances
            +
            1.0
        )
        /
        (
            len(null_alphas)
            +
            1.0
        )
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
                    null_alphas
                    -
                    real_alpha
                )
                <
                robust_sigma
            )
        )

    else:
        overlap_score = float(
            np.mean(
                null_alphas
                ==
                real_alpha
            )
        )

    if abs(median_null) > 0:
        relative_gap = float(
            absolute_gap
            /
            abs(median_null)
        )

    else:
        relative_gap = None

    distribution_distance = float(
        wasserstein_distance(
            null_alphas,
            np.repeat(
                real_alpha,
                len(null_alphas),
            ),
        )
    )

    if (
        z_valid
        and
        not null_degenerate
    ):
        z_interpretation = (
            "valid_robust_separation_against_"
            "supplied_null_diagnostic"
        )

    else:
        z_interpretation = (
            "z_score_not_interpretable_as_strength"
        )

    return {
        "real_alpha": float(
            real_alpha
        ),
        "null_median": median_null,
        "null_q1": q1,
        "null_q3": q3,
        "robust_sigma": robust_sigma,
        "gap": absolute_gap,
        "alpha_z_score": z_score,
        "z_score_valid": bool(
            z_valid
        ),
        "z_score_interpretation": z_interpretation,
        "evidence_role":
            "diagnostic_only",
        "independent_evidence":
            False,
        "null_relationship":
            (
                "This separation diagnostic uses a "
                "supplied permutation-null ensemble. "
                "When the primary statistical endpoint "
                "uses the same permutation-null family, "
                "this diagnostic is not an independent "
                "replication of that inference."
            ),
        "interpretation":
            (
                "Observed alpha is separated from the "
                "supplied permutation-null ensemble as "
                "a secondary diagnostic. This does not "
                "constitute independent evidence and does "
                "not establish mechanism, universality, "
                "consciousness, NEF, HCM causation, or "
                "external reproducibility."
            ),
        "null_degenerate":
            null_degenerate,
        "empirical_p_upper":
            empirical_p_upper,
        "null_exceedances":
            int(exceedances),
        "percentile_rank":
            percentile_rank,
        "overlap_score":
            overlap_score,
        "relative_gap":
            relative_gap,
        "fingerprint_distance_mean":
            (
                float(
                    np.mean(
                        fp_distances
                    )
                )
                if len(fp_distances)
                else np.nan
            ),
        "wasserstein_distance":
            distribution_distance,
        "null_count":
            int(
                len(null_alphas)
            ),
    }
