import numpy as np
# 🔥 smoothing
from scipy.ndimage import uniform_filter1d

def estimate_alpha(series):
    series = np.asarray(series)
    series = series - np.mean(series)
    n = len(series)

    if n < 32:
        return np.nan

    window = np.hanning(n)
    series = series * window

    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / n
    freqs = np.fft.rfftfreq(n)

    mask = (freqs > 0.02) & (freqs < 0.25)

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 10:
        return np.nan

    psd = uniform_filter1d(psd, size=7)

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-10)

    # 🔥 robust fit (median slope)
    slopes = []
    for i in range(len(log_f) - 5):
        x = log_f[i:i+5]
        y = log_psd[i:i+5]
        A = np.vstack([x, np.ones(len(x))]).T
        slope, _ = np.linalg.lstsq(A, y, rcond=None)[0]
        slopes.append(slope)

    slope = np.median(slopes)

    return float(-slope)

def block_bootstrap(series, block_size=16, num_boot=100):
    n = len(series)
    alphas = []

    for _ in range(num_boot):
        sample = []
        while len(sample) < n:
            start = np.random.randint(0, n - block_size)
            block = series[start:start+block_size]
            sample.extend(block)

        sample = np.array(sample[:n])
        alphas.append(estimate_alpha(sample))

    alphas = np.array(alphas)

    return {
        "mean": float(np.mean(alphas)),
        "std": float(np.std(alphas)),
        "ci_low": float(np.percentile(alphas, 2.5)),
        "ci_high": float(np.percentile(alphas, 97.5))
    }
