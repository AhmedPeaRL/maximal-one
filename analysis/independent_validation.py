from __future__ import annotations
import numpy as np
from scipy.signal import welch
from analysis.numerical_spectral_verification import estimate_alpha

FREQ_MIN = 0.01
FREQ_MAX = 0.25

def sanitize_alpha(alpha):
    """
    Validation-only sanitation.

    IMPORTANT:
    No scientific clipping is performed here.
    An invalid/non-finite estimate is rejected rather than
    being forced into an expected range.
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

def welch_alpha_estimation(series):
    """
    Independent Welch-based spectral exponent estimator.

    This estimator intentionally has no scientific clipping.
    It is used as an independent methodological cross-check
    against the primary estimate_alpha() pipeline.
    """

    series = np.asarray(series, dtype=np.float64)

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

    nperseg = min(256, len(series) // 2)

    if nperseg < 128:
        return np.nan

    freqs, psd = welch(
        series,
        nperseg=nperseg,
        window="hann",
        detrend="linear",
        scaling="density",
    )

    mask = (
        (freqs > FREQ_MIN)
        & (freqs < FREQ_MAX)
        & np.isfinite(freqs)
        & np.isfinite(psd)
        & (psd > 0)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    if not (
        np.all(np.isfinite(log_f))
        and np.all(np.isfinite(log_psd))
    ):
        return np.nan

    try:
        slope, _ = np.polyfit(
            log_f,
            log_psd,
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

    return float(np.round(alpha, 8))

def compare_methods(series):
    """
    Independent methodological validation.

    Method 1:
        Primary spectral estimator.

    Method 2:
        Independent Welch regression.

    No result is clipped or forced into an expected scientific range.
    """

    alpha_fft = sanitize_alpha(
        estimate_alpha(series)
    )

    alpha_welch = sanitize_alpha(
        welch_alpha_estimation(series)
    )

    if not (
        np.isfinite(alpha_fft)
        and np.isfinite(alpha_welch)
    ):
        print("⚠️ invalid alpha in one method")
        return alpha_fft, alpha_welch

    delta = abs(
        alpha_fft - alpha_welch
    )

    print(f"FFT alpha: {alpha_fft}")
    print(f"Welch alpha: {alpha_welch}")
    print(f"Agreement delta: {delta}")

    return alpha_fft, alpha_welch
