from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)

# Canonical temporal aggregation scales.
SCALES = (1, 2, 4, 8)

# Canonical spectral comparison band in the ORIGINAL
# sampling units.
BASE_FREQ_MIN = 0.01
BASE_FREQ_MAX = 0.05

# Upper normalized frequency allowed after rescaling.
# We deliberately stay below Nyquist.
MAX_NORMALIZED_FREQ = 0.45

MAX_PAIRWISE_DELTA = 0.50
MAX_RELATIVE_SPREAD = 0.40

primary_alpha = float(alphas[0])
    max_primary_scale_delta = float(
        np.max(
            np.abs(
                alphas - primary_alpha
            )
        )
    )
    primary_scale_ratio = float(
        max_primary_scale_delta
        /
        max(
            abs(primary_alpha),
            1e-12
        )
    )

def downsample(series, factor):
    """
    Temporal aggregation by non-overlapping block averaging.

    This changes the sampling interval by `factor`.
    No interpolation or synthetic padding is introduced.
    """

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
    """
    Map the canonical ORIGINAL-sampling frequency band
    into the frequency coordinates of the aggregated series.

    If the sampling interval becomes `scale` times larger,
    a physical/original frequency f appears at:

        f_scaled = f * scale

    We therefore compare the same original physical band
    across scales.

    The upper bound is restricted below Nyquist.
    """

    lower = (
        BASE_FREQ_MIN
        * float(scale)
    )

    upper = min(
        BASE_FREQ_MAX
        * float(scale),
        MAX_NORMALIZED_FREQ,
    )

    if not (
        np.isfinite(lower)
        and np.isfinite(upper)
        and lower > 0.0
        and upper > lower
        and upper < 0.5
    ):
        return None

    return (
        float(lower),
        float(upper),
    )

def multi_scale_alpha(series):
    """
    Estimate spectral persistence across temporal aggregation scales.

    IMPORTANT:
    This is a temporal-scale test, not merely a test of numerical
    stability under array resizing.

    The same ORIGINAL physical frequency band is mapped into the
    frequency coordinates of each aggregated series.

    No reflect-padding is performed here because padding creates
    synthetic observations and can alter the spectrum.
    """

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
            scaled = series.copy()
        else:
            scaled = downsample(
                series,
                scale,
            )

        # Do not manufacture observations merely to satisfy
        # the estimator. The measurement must remain based on
        # actually observed/aggregated samples.
        if len(scaled) < 256:
            continue

        freq_band = _scale_frequency_band(
            scale
        )

        if freq_band is None:
            continue

        freq_min, freq_max = freq_band

        scaled = np.asarray(
            scaled,
            dtype=np.float64,
        )

        scaled = (
            scaled
            - np.mean(scaled)
        )

        std = np.std(scaled)

        if std < 1e-12:
            continue

        scaled = scaled / std

        from scipy.signal import welch

        nperseg = min(
            1024,
            len(scaled),
        )

        if nperseg < 128:
            continue

        freqs, psd = welch(
            scaled,
            nperseg=nperseg,
            window="hann",
            detrend="linear",
            scaling="density",
        )

        mask = (
            (freqs > freq_min)
            &
            (freqs < freq_max)
            &
            np.isfinite(freqs)
            &
            np.isfinite(psd)
            &
            (psd > 0)
        )

        if np.sum(mask) < 20:
            continue

        alpha = float(
            -np.polyfit(
                np.log(freqs[mask]),
                np.log(psd[mask]),
                1,
            )[0]
        )

        if np.isfinite(alpha):
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
        [item[0] for item in results],
        dtype=np.int64,
    )

    alphas = np.asarray(
        [item[1] for item in results],
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

    if np.any(alphas < 0):
        return {
            "valid": False,
            "reason": "negative_scale_alpha",
            "scale_invariant": False,
            "dispersion": np.nan,
            "scales": [],
        }

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

        "primary_scale_diagnostic": {
            "primary_alpha": primary_alpha,
            "max_absolute_delta": max_primary_scale_delta,
            "relative_delta": primary_scale_ratio,
            "interpretation": (
                "diagnostic_only: compares the scale-1 "
                "estimate with temporally aggregated estimates"
            )
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
            "base_frequency_min": BASE_FREQ_MIN,
            "base_frequency_max": BASE_FREQ_MAX,
            "max_normalized_frequency":
                MAX_NORMALIZED_FREQ,
            "interpretation":
                "same_original_frequency_band_mapped "
                "into each temporally aggregated series"
        },

        "median_alpha": median_alpha,
        "q1_alpha": q1,
        "q3_alpha": q3,
        "mad_alpha": float(mad),
        "robust_sigma": robust_sigma,
        "pairwise_delta": pairwise_delta,
        "relative_spread": relative_spread,
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
