from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
    DEFAULT_FREQ_MIN,
    DEFAULT_FREQ_MAX,
)

# ============================================================
# CANONICAL TEMPORAL SCALES
# ============================================================

SCALES = (1, 2, 4, 8)

BASE_FREQ_MIN = DEFAULT_FREQ_MIN
BASE_FREQ_MAX = DEFAULT_FREQ_MAX

MAX_NORMALIZED_FREQ = 0.45

MAX_PAIRWISE_DELTA = 0.50
MAX_RELATIVE_SPREAD = 0.40

def downsample(series, factor):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if factor < 1:
        raise ValueError(
            "factor must be >= 1"
        )

    if series.ndim != 1:
        raise ValueError(
            "series must be one-dimensional"
        )

    n = len(series) // factor

    if n < 1:
        return np.asarray(
            [],
            dtype=np.float64,
        )

    trimmed = series[
        : n * factor
    ]

    return trimmed.reshape(
        n,
        factor,
    ).mean(axis=1)

def _scale_frequency_band(scale):
    lower = (
        BASE_FREQ_MIN
        * float(scale)
    )

    upper = (
        BASE_FREQ_MAX
        * float(scale)
    )

    if not (
        np.isfinite(lower)
        and
        np.isfinite(upper)
        and
        lower > 0.0
        and
        upper > lower
        and
        upper < 0.5
    ):
        return None

    return (
        float(lower),
        float(upper),
    )

def multi_scale_alpha(series):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        return []

    if not np.all(
        np.isfinite(series)
    ):
        return []

    results = []

    for scale in SCALES:

        if scale == 1:

            # ====================================================
            # ABSOLUTE PROTOCOL REQUIREMENT
            #
            # scale=1 MUST use the exact canonical estimator.
            # ====================================================

            alpha = estimate_alpha(
                series,
                freq_min=BASE_FREQ_MIN,
                freq_max=BASE_FREQ_MAX,
            )

            if not np.isfinite(alpha):
                continue

            results.append(
                (
                    1,
                    float(alpha),
                    float(BASE_FREQ_MIN),
                    float(BASE_FREQ_MAX),
                    int(len(series)),
                )
            )

            continue

        scaled = downsample(
            series,
            scale,
        )

        if len(scaled) < 256:
            continue

        freq_band = _scale_frequency_band(
            scale
        )

        if freq_band is None:
            continue

        freq_min, freq_max = freq_band

        alpha = estimate_alpha(
            scaled,
            freq_min=freq_min,
            freq_max=freq_max,
        )

        if not np.isfinite(alpha):
            continue

        results.append(
            (
                int(scale),
                float(alpha),
                float(freq_min),
                float(freq_max),
                int(len(scaled)),
            )
        )

    return results

def evaluate_scale_invariance(series):
    results = multi_scale_alpha(
        series
    )

    if len(results) < 3:
        return {
            "valid": False,
            "reason": "insufficient_scales",
            "scale_invariant": False,
            "dispersion": np.nan,
            "scales": [],
        }

    scales = np.asarray(
        [
            item[0]
            for item in results
        ],
        dtype=np.int64,
    )

    alphas = np.asarray(
        [
            item[1]
            for item in results
        ],
        dtype=np.float64,
    )

    if not np.all(
        np.isfinite(alphas)
    ):
        return {
            "valid": False,
            "reason": "non_finite_scale_alpha",
            "scale_invariant": False,
            "dispersion": np.nan,
            "scales": [],
        }

    # ============================================================
    # HARD INTERNAL CONSISTENCY CHECK
    # ============================================================

    canonical_alpha = estimate_alpha(
        series,
        freq_min=BASE_FREQ_MIN,
        freq_max=BASE_FREQ_MAX,
    )

    if not np.isfinite(canonical_alpha):
        return {
            "valid": False,
            "reason": "canonical_alpha_unavailable",
            "scale_invariant": False,
            "dispersion": np.nan,
            "scales": [],
        }

    scale_one_indices = np.where(
        scales == 1
    )[0]

    if len(scale_one_indices) != 1:
        return {
            "valid": False,
            "reason": "scale_one_missing_or_duplicated",
            "scale_invariant": False,
            "dispersion": np.nan,
            "scales": [],
        }

    scale_one_alpha = float(
        alphas[
            scale_one_indices[0]
        ]
    )

    internal_delta = abs(
        scale_one_alpha
        -
        float(canonical_alpha)
    )

    if internal_delta > 1e-8:
        return {
            "valid": False,
            "reason": "scale_one_not_identical_to_canonical",
            "scale_invariant": False,
            "dispersion": np.nan,
            "scales": [],
            "canonical_alpha": float(
                canonical_alpha
            ),
            "scale_one_alpha": scale_one_alpha,
            "internal_delta": internal_delta,
        }

    primary_alpha = float(
        canonical_alpha
    )

    max_primary_scale_delta = float(
        np.max(
            np.abs(
                alphas
                -
                primary_alpha
            )
        )
    )

    primary_scale_ratio = float(
        max_primary_scale_delta
        /
        max(
            abs(primary_alpha),
            1e-12,
        )
    )

    median_alpha = float(
        np.median(alphas)
    )

    q1 = float(
        np.percentile(
            alphas,
            25,
        )
    )

    q3 = float(
        np.percentile(
            alphas,
            75,
        )
    )

    mad = float(
        np.median(
            np.abs(
                alphas
                -
                median_alpha
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
        max(
            abs(median_alpha),
            1e-12,
        )
    )

    dispersion = relative_spread

    scale_invariant = bool(
        pairwise_delta
        <= MAX_PAIRWISE_DELTA
        and
        relative_spread
        <= MAX_RELATIVE_SPREAD
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

        "canonical_alpha": float(
            canonical_alpha
        ),

        "scale_one_alpha": scale_one_alpha,

        "scale_one_internal_delta":
            float(internal_delta),

        "primary_scale_diagnostic": {
            "primary_alpha": primary_alpha,
            "max_absolute_delta":
                max_primary_scale_delta,
            "relative_delta":
                primary_scale_ratio,
            "interpretation":
                "scale=1 is exactly the canonical "
                "Welch estimator; other scales are "
                "evaluated after temporal aggregation "
                "using the same estimator and mapped "
                "physical frequency band",
        },

        "scales": [
            {
                "scale": int(item[0]),
                "alpha": float(item[1]),
                "frequency_min": float(item[2]),
                "frequency_max": float(item[3]),
                "sample_count": int(item[4]),
            }
            for item in results
        ],

        "frequency_comparison": {
            "base_frequency_min":
                BASE_FREQ_MIN,
            "base_frequency_max":
                BASE_FREQ_MAX,
            "max_normalized_frequency":
                MAX_NORMALIZED_FREQ,
            "interpretation":
                "same original physical frequency "
                "band mapped into each temporally "
                "aggregated series",
        },

        "median_alpha":
            median_alpha,

        "q1_alpha":
            q1,

        "q3_alpha":
            q3,

        "mad_alpha":
            float(mad),

        "robust_sigma":
            robust_sigma,

        "pairwise_delta":
            pairwise_delta,

        "relative_spread":
            relative_spread,

        "dispersion":
            dispersion,

        "max_pairwise_delta":
            MAX_PAIRWISE_DELTA,

        "max_relative_spread":
            MAX_RELATIVE_SPREAD,

        "scale_invariant":
            scale_invariant,

        "diagnostics":
            diagnostics,
    }

if __name__ == "__main__":
    print(
        "multi_scale_validation.py loaded successfully"
    )
