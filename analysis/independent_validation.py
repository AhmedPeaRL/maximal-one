import numpy as np
from scipy.signal import welch
from scipy.stats import linregress


def sanitize_alpha(alpha):

    if not np.isfinite(alpha):
        return np.nan

    alpha = float(alpha)

    alpha = np.clip(alpha, 0.0, 5.0)

    return float(alpha)


def estimate_alpha_welch(series):

    series = np.asarray(
        series,
        dtype=np.float64
    )

    if not np.all(np.isfinite(series)):
        return np.nan

    n = len(series)

    if n < 64:
        return np.nan

    series = series - np.mean(series)

    freqs, psd = welch(
        series,
        nperseg=min(128, n),
        scaling="density",
        window="hann",
        detrend="constant"
    )

    mask = (
        (freqs > 0.01)
        & (freqs < 0.35)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 12:
        return np.nan

    psd = np.maximum(psd, 1e-12)

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    slope, _, _, _, _ = linregress(
        log_f,
        log_psd
    )

    if not np.isfinite(slope):
        return np.nan

    if slope > 0:
        slope = -abs(slope)

    alpha = -slope

    return sanitize_alpha(alpha)


def compare_methods(series):

    from analysis.numerical_spectral_verification import (
        estimate_alpha
    )

    fft_alpha = sanitize_alpha(
        estimate_alpha(series)
    )

    welch_alpha = sanitize_alpha(
        estimate_alpha_welch(series)
    )

    if len(segment) < 64:
    continue

    print(f"Method 1 (FFT): {fft_alpha}")
    print(f"Method 2 (Welch): {welch_alpha}")

    return fft_alpha, welch_alpha
