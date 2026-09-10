from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
    DEFAULT_FREQ_MIN,
    DEFAULT_FREQ_MAX,
)

FREEZE_DECIMALS = 8

FREQ_MIN = DEFAULT_FREQ_MIN
FREQ_MAX = DEFAULT_FREQ_MAX

def sanitize_alpha(alpha):
    if alpha is None:
        return np.nan

    try:
        alpha = float(alpha)
    except (
        TypeError,
        ValueError,
    ):
        return np.nan

    if not np.isfinite(alpha):
        return np.nan

    return alpha

def periodogram_alpha_estimation(series):
    """
    Independent FFT-periodogram spectral exponent estimator.

    The method remains independent from Welch, while using the
    SAME declared physical frequency band.

    No clipping.
    No forced agreement.
    """

    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        return np.nan

    if len(series) < 256:
        return np.nan

    if not np.all(
        np.isfinite(series)
    ):
        return np.nan

    series = (
        series
        - np.mean(series)
    )

    std = np.std(series)

    if std < 1e-12:
        return np.nan

    series = (
        series
        / std
    )

    n = len(series)

    fft = np.fft.rfft(
        series
    )

    power = (
        np.abs(fft) ** 2
    ) / float(n)

    freqs = np.fft.rfftfreq(
        n
    )

    mask = (
        (freqs > FREQ_MIN)
        &
        (freqs < FREQ_MAX)
        &
        np.isfinite(freqs)
        &
        np.isfinite(power)
        &
        (power > 0)
    )

    freqs = freqs[mask]
    power = power[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_power = np.log(power)

    if not (
        np.all(np.isfinite(log_f))
        and
        np.all(np.isfinite(log_power))
    ):
        return np.nan

    try:
        slope, _ = np.polyfit(
            log_f,
            log_power,
            1,
        )
    except Exception:
        return np.nan

    slope = float(
        slope
    )

    if not np.isfinite(slope):
        return np.nan

    alpha = -slope

    if not np.isfinite(alpha):
        return np.nan

    return float(
        np.round(
            alpha,
            FREEZE_DECIMALS,
        )
    )

def compare_methods(series):
    alpha_primary = sanitize_alpha(
        estimate_alpha(series)
    )

    alpha_independent = sanitize_alpha(
        periodogram_alpha_estimation(
            series
        )
    )

    if not (
        np.isfinite(alpha_primary)
        and
        np.isfinite(alpha_independent)
    ):
        print(
            "⚠️ invalid alpha in one method"
        )

        return (
            alpha_primary,
            alpha_independent,
        )

    delta = abs(
        alpha_primary
        -
        alpha_independent
    )

    print(
        f"Primary Welch alpha: {alpha_primary}"
    )

    print(
        f"Independent FFT alpha: "
        f"{alpha_independent}"
    )

    print(
        f"Agreement delta: {delta}"
    )

    return (
        alpha_primary,
        alpha_independent,
    )

# Legacy compatibility.
core_alpha_estimation = (
    periodogram_alpha_estimation
)
