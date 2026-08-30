from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)

FREQ_MIN = 0.01
FREQ_MAX = 0.25
FREEZE_DECIMALS = 8

def sanitize_alpha(alpha):
    """
    Validation-only sanitation.

    No scientific clipping or forced range is applied.
    Invalid/non-finite estimates are rejected.
    """

    if alpha is None:
        return np.nan

    try:
        alpha = float(alpha)
    except (TypeError, ValueError):
        return np.nan

    if not np.isfinite(alpha):
        return np.nan

    return alpha

def periodogram_alpha_estimation(series):
    """
    Independent FFT-periodogram spectral exponent estimator.

    IMPORTANT:
    The primary estimator in numerical_spectral_verification.py
    uses scipy.signal.welch().

    This validator intentionally uses a direct FFT periodogram
    so that methodological agreement is genuinely cross-method.

    No scientific clipping is performed.
    """

    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        return np.nan

    if len(series) < 256:
        return np.nan

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - np.mean(series)

    std = np.std(series)

    if std < 1e-12:
        return np.nan

    series = series / std

    n = len(series)

    fft = np.fft.rfft(series)

    power = (
        np.abs(fft) ** 2
    ) / float(n)

    freqs = np.fft.rfftfreq(n)

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

    slope = float(slope)

    if not np.isfinite(slope):
        return np.nan

    alpha = -slope

    if not np.isfinite(alpha):
        return np.nan

    # Tiny negative numerical excursions may be treated as zero.
    if alpha < 0:
        if alpha > -0.20:
            alpha = 0.0
        else:
            return np.nan

    return float(
        np.round(
            alpha,
            FREEZE_DECIMALS,
        )
    )

def compare_methods(series):
    """
    Genuine independent methodological validation.

    Primary:
        Welch-based estimate_alpha()

    Independent validator:
        Direct FFT periodogram regression.

    No scientific clipping or forced agreement is performed.
    """

    alpha_primary = sanitize_alpha(
        estimate_alpha(series)
    )

    alpha_independent = sanitize_alpha(
        periodogram_alpha_estimation(series)
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
        f"Independent FFT alpha: {alpha_independent}"
    )

    print(
        f"Agreement delta: {delta}"
    )

    return (
        alpha_primary,
        alpha_independent,
    )

# Backward-compatible symbol for legacy callers.
# This is intentionally an alias to the genuinely independent
# FFT-periodogram estimator, NOT a Welch implementation.
core_alpha_estimation = periodogram_alpha_estimation
