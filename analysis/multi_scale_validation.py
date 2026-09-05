from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)

SCALES = (1, 2, 4, 8)

MAX_PAIRWISE_DELTA = 0.50
MAX_RELATIVE_SPREAD = 0.40

def downsample(series, factor):
    series = np.asarray(series, dtype=np.float64)

    if factor < 1:
        raise ValueError("factor must be >= 1")

    n = len(series) // factor

    if n < 1:
        return np.asarray([], dtype=np.float64)

    trimmed = series[: n * factor]

    return trimmed.reshape(n, factor).mean(axis=1)

def multi_scale_alpha(series):
    series = np.asarray(series, dtype=np.float64)

    if series.ndim != 1:
        return []

    if not np.all(np.isfinite(series)):
        return []

    results = []

    for scale in SCALES:

        if scale == 1:
            scaled = series.copy()

        else:
            scaled = downsample(
                series,
                scale,
            )

        if len(scaled) < 64:
            continue

        # Padding is retained only to satisfy
        # the estimator's minimum-length requirement.
        if len(scaled) < 256:
            scaled = np.pad(
                scaled,
                (0, 256 - len(scaled)),
                mode="reflect",
            )

        alpha = estimate_alpha(scaled)

        if np.isfinite(alpha):
            results.append(
                (
                    int(scale),
                    float(alpha),
                )
            )

    return results

def evaluate_scale_invariance(series):
    results = multi_scale_alpha(series)

    if len(results) < 3:
        return {
            "valid": False,
            "reason": "insufficient_scales",
            "scale_invariant": False,
            "dispersion": np.nan,
        }

    scales = np.asarray(
        [s for s, _ in results],
        dtype=np.int64,
    )

    alphas = np.asarray(
        [a for _, a in results],
        dtype=np.float64,
    )

    if not np.all(np.isfinite(alphas)):
        return {
            "valid": False,
            "reason": "non_finite_scale_alpha",
            "scale_invariant": False,
            "dispersion": np.nan,
        }

    if np.any(alphas < 0):
        return {
            "valid": False,
            "reason": "negative_scale_alpha",
            "scale_invariant": False,
            "dispersion": np.nan,
        }

    median_alpha = float(
        np.median(alphas)
    )

    q1 = float(
        np.percentile(alphas, 25)
    )

    q3 = float(
        np.percentile(alphas, 75)
    )

    mad = float(
        np.median(
            np.abs(
                alphas - median_alpha
            )
        )
    )

    robust_sigma = float(
        1.4826 * mad
    )

    pairwise_delta = float(
        np.max(alphas)
        -
        np.min(alphas)
    )

    relative_spread = float(
        pairwise_delta
        /
        max(abs(median_alpha), 1e-12)
    )

    # ---------------------------------------------------------
    # Canonical dispersion definition
    #
    # "dispersion" is explicitly defined as the relative
    # spread across the evaluated scales.
    #
    # This is the quantity used by downstream evidence and
    # consensus layers.
    # ---------------------------------------------------------

    dispersion = relative_spread

    scale_invariant = bool(
        pairwise_delta <= MAX_PAIRWISE_DELTA
        and
        relative_spread <= MAX_RELATIVE_SPREAD
    )

    diagnostics = []

    if pairwise_delta > MAX_PAIRWISE_DELTA:
        diagnostics.append(
            "pairwise_scale_delta_exceeded"
        )

    if relative_spread > MAX_RELATIVE_SPREAD:
        diagnostics.append(
            "relative_scale_spread_exceeded"
        )

    return {
        "valid": True,

        "scales": [
            [
                int(scale),
                float(alpha),
            ]
            for scale, alpha in results
        ],

        "median_alpha": median_alpha,

        "q1_alpha": q1,

        "q3_alpha": q3,

        "mad_alpha": float(mad),

        "robust_sigma": robust_sigma,

        "pairwise_delta": pairwise_delta,

        "relative_spread": relative_spread,

        # Canonical downstream field.
        "dispersion": dispersion,

        "max_pairwise_delta":
            MAX_PAIRWISE_DELTA,

        "max_relative_spread":
            MAX_RELATIVE_SPREAD,

        "scale_invariant":
            scale_invariant,

        "diagnostics":
            diagnostics,
    }
