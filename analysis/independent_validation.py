import numpy as np
from scipy.signal import welch
from scipy.stats import linregress

FREQ_MIN = 0.02
FREQ_MAX = 0.25

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
        detrend="constant",
        average="median"
    )

    mask = (
        (freqs > FREQ_MIN)
        & (freqs < FREQ_MAX)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 12:
        return np.nan

    psd = np.convolve(
        psd,
        np.ones(3) / 3,
        mode="same"
    )

    psd = np.round(psd, 8)

    psd = np.maximum(psd, 1e-12)

    log_f = np.round(
        np.log(freqs),
        8
    )

    log_psd = np.round(
        np.log(psd),
        8
    )

    slopes = []

    window = 5

    for i in range(len(log_f) - window):

        x = log_f[i:i + window]
        y = log_psd[i:i + window]

        if np.std(y) < 1e-8:
            continue

        try:

            coeffs = np.polyfit(
                x,
                y,
                1
            )

            slope = float(
                np.round(coeffs[0], 8)
            )

            if np.isfinite(slope):
                slopes.append(slope)

        except Exception:
            continue

    if len(slopes) < 6:
        return np.nan

    slopes = np.asarray(
        slopes,
        dtype=np.float64
    )

    median = np.median(slopes)

    mad = np.median(
        np.abs(slopes - median)
    ) + 1e-12

    filtered = slopes[
        np.abs(slopes - median)
        < 2.5 * mad
    ]

    if len(filtered) < 4:
        filtered = slopes

    slope = np.mean(filtered)

    if slope > 0:
        slope = -abs(slope)

    alpha = -slope

    return float(
        np.round(
            sanitize_alpha(alpha),
            8
        )
    )

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

    agreement_delta = abs(
        fft_alpha - welch_alpha
    )

    print(f"Method 1 (FFT): {fft_alpha}")
    print(f"Method 2 (Welch): {welch_alpha}")
    print(f"Agreement delta: {agreement_delta}")

    return fft_alpha, welch_alpha
