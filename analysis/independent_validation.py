import numpy as np
from scipy.signal import welch
from scipy.stats import linregress

def estimate_alpha_welch(series):

    series = np.asarray(series, dtype=np.float64)

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - np.mean(series)

    n = len(series)

    if n < 32:
        return np.nan

    nperseg = min(64, n)

    freqs, psd = welch(
        series,
        nperseg=nperseg,
        scaling="density",
        window="hann",
        detrend="constant"
    )

    mask = (freqs > 0.02) & (freqs < 0.25)

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 10:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-10)

    slope, _, _, _, _ = linregress(log_f, log_psd)

    alpha = float(-slope)

    if not np.isfinite(alpha):
        return np.nan

    return alpha

def compare_methods(series):

    from analysis.numerical_spectral_verification import (
        estimate_alpha
    )

    fft_alpha = estimate_alpha(series)

    welch_alpha = estimate_alpha_welch(series)

    print(f"Method 1 (FFT): {fft_alpha}")
    print(f"Method 2 (Welch): {welch_alpha}")

    return fft_alpha, welch_alpha    
