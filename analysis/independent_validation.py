from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha,
    DEFAULT_FREQ_MIN,
    DEFAULT_FREQ_MAX,
    CANONICAL_MIN_BINS,
)

FREEZE_DECIMALS = 8

FREQ_MIN = DEFAULT_FREQ_MIN
FREQ_MAX = DEFAULT_FREQ_MAX

def sanitize_alpha(alpha):
    if alpha is None:
        return np.nan

    try:
        alpha = float(alpha)
    except (TypeError, ValueError):
        return np.nan

    if not np.isfinite(alpha):
        return np.nan

    return alpha

def _prepare_series(series):
    series = np.asarray(series, dtype=np.float64)

    if series.ndim != 1:
        return None

    if len(series) < 256:
        return None

    if not np.all(np.isfinite(series)):
        return None

    mean = np.mean(series)

    if not np.isfinite(mean):
        return None

    series = series - mean

    std = np.std(series)

    if not np.isfinite(std) or std < 1e-12:
        return None

    return series / std

def periodogram_alpha_estimation(series):
    """
    Independent full-series FFT periodogram estimator.

    This estimator intentionally remains mathematically
    distinct from the canonical Welch estimator.

    No clipping.
    No forced agreement.
    No post-hoc correction.
    No range correction.

    The returned disagreement with Welch is empirical evidence
    and must remain observable.
    """

    series = _prepare_series(series)

    if series is None:
        return np.nan

    n = len(series)

    fft = np.fft.rfft(series)

    power = (np.abs(fft) ** 2) / float(n)

    freqs = np.fft.rfftfreq(n)

    mask = (
        (freqs > FREQ_MIN)
        & (freqs < FREQ_MAX)
        & np.isfinite(freqs)
        & np.isfinite(power)
        & (power > 0)
    )

    freqs = freqs[mask]
    power = power[mask]

    if len(freqs) < CANONICAL_MIN_BINS:
        return np.nan

    log_f = np.log(freqs)
    log_power = np.log(power)

    if not (
        np.all(np.isfinite(log_f))
        and np.all(np.isfinite(log_power))
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

    return float(
        np.round(
            alpha,
            FREEZE_DECIMALS,
        )
    )

def compare_methods(series):
    """
    Compare the canonical Welch estimator with the
    independent full-series FFT periodogram.

    IMPORTANT:
    This function does not attempt to make the estimators agree.

    Any disagreement is reported exactly as observed.
    """

    welch_alpha = sanitize_alpha(
        estimate_alpha(series)
    )

    fft_alpha = sanitize_alpha(
        periodogram_alpha_estimation(series)
    )

    if not (
        np.isfinite(welch_alpha)
        and np.isfinite(fft_alpha)
    ):
        return {
            "welch_alpha": float(welch_alpha),
            "fft_alpha": float(fft_alpha),
            "delta": np.nan,
            "finite": False,
            "agreement": False,
        }

    delta = abs(
        welch_alpha - fft_alpha
    )

    return {
        "welch_alpha": float(welch_alpha),
        "fft_alpha": float(fft_alpha),
        "delta": float(
            np.round(
                delta,
                FREEZE_DECIMALS,
            )
        ),
        "finite": True,
        "agreement": bool(
            delta <= 0.30
        ),
        "threshold": 0.30,
    }

# Legacy compatibility.
core_alpha_estimation = (
    periodogram_alpha_estimation
)
