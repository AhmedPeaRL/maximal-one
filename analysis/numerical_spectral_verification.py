import numpy as np
# 🔥 smoothing
from scipy.ndimage import uniform_filter1d

def estimate_alpha(series):
    series = np.asarray(series)
    series = series - np.mean(series)
    n = len(series)

    window = np.hanning(n)
    series = series * window

    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / n
    freqs = np.fft.rfftfreq(n)

    mask = (freqs > 0.01) & (freqs < 0.3)
    freqs = freqs[mask]
    psd = psd[mask]
    psd = uniform_filter1d(psd, size=5)

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    # linear regression حقيقية
    A = np.vstack([log_f, np.ones(len(log_f))]).T
    slope, intercept = np.linalg.lstsq(A, log_psd, rcond=None)[0]

    alpha = -slope
    return float(alpha)

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
