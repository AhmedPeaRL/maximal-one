import numpy as np
# 🔥 smoothing
from scipy.ndimage import uniform_filter1d
from scipy.signal import welch

np.set_printoptions(precision=15)

def estimate_alpha(series):
    series = np.asarray(series, dtype=np.float64)

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - np.mean(series)

    n = len(series)

    if n < 32:
        return np.nan

    # windowing
    window = np.hanning(n)
    series = series * window

    freqs = np.fft.rfftfreq(n)

    mask = (freqs > 0.02) & (freqs < 0.25)

    if np.sum(mask) < 10:
        return np.nan

    from analysis.deterministic_ops import (
        stable_smoothing,
        stable_fft_power,
        stable_log,
        stable_polyfit
    )

    psd_full = stable_fft_power(series)

    psd_full = stable_smoothing(psd_full)

    # 🔥 spectral floor stabilization
    psd_full = np.maximum(psd_full, 1e-12)

    psd_full = np.round(psd_full, 10)

    psd = psd_full[mask]
    freqs = freqs[mask]

    if len(psd) < 10:
        return np.nan

    if np.any(psd <= 0):
        return np.nan

    log_f = stable_log(freqs)
    log_psd = stable_log(psd)

    # global spectral fit
    slope = stable_polyfit(
        log_f,
        log_psd
    )

    if not np.isfinite(slope):
        return np.nan

    # 🔥 relaxed physical guard
    if slope > 0.25:
        return np.nan

    alpha = float(-slope)

    if not np.isfinite(alpha):
        return np.nan

    if alpha < 0.05 or alpha > 6:
        return np.nan

    return alpha

def estimate_alpha_welch(series):
    series = np.asarray(series, dtype=np.float64)

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - np.mean(series)

    n = len(series)
    if n < 32:
        return np.nan

    freqs, psd = welch(
        series,
        nperseg=min(256, n),
        scaling="density",
        window="hann",
        detrend="constant"
    )

    # نفس الـ mask بالظبط
    mask = (freqs > 0.02) & (freqs < 0.25)
    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 10:
        return np.nan

    # 🔥 نفس الـ smoothing
    psd = uniform_filter1d(psd, size=2)
    psd = np.round(psd, 10)

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-10)

    slopes = []
    for i in range(len(log_f) - 5):
        x = log_f[i:i+5]
        y = log_psd[i:i+5]
        A = np.vstack([x, np.ones(len(x))]).T
        coeffs = np.polyfit(x, y, 1)
        slope = coeffs[0]
        slopes.append(slope)

    slopes = np.array(slopes)
    slopes = slopes[np.isfinite(slopes)]

    if len(slopes) < 5:
        return np.nan

    slope = np.median(slopes)

    if not np.isfinite(slope) or slope > 0:
        return np.nan

    alpha = float(-slope)

    if not np.isfinite(alpha):
        return np.nan

    return alpha

def block_bootstrap(series, rng, block_size=16, num_boot=100):
    n = len(series)
    alphas = []

    for _ in range(num_boot):
        sample = []
        while len(sample) < n:
            start = rng.randint(0, n - block_size)
            block = series[start:start+block_size]
            sample.extend(block)

        sample = np.array(sample[:n])
        alphas.append(estimate_alpha(sample))

    alphas = np.array(alphas)
    alphas = alphas[np.isfinite(alphas)]

    if len(alphas) < 10:
        return {
            "mean": float(np.nanmean(alphas)) if len(alphas) > 0 else np.nan,
            "std": float(np.nanstd(alphas)) if len(alphas) > 0 else np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan
        }

    return {
        "mean": float(np.mean(alphas)),
        "std": float(np.std(alphas)),
        "ci_low": float(np.percentile(alphas, 2.5)),
        "ci_high": float(np.percentile(alphas, 97.5))
    }
