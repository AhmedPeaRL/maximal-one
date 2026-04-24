import numpy as np

def estimate_alpha(series):
    """
    Robust spectral alpha estimation
    """

    series = series - np.mean(series)
    n = len(series)

    window = np.hanning(n)
    series = series * window

    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / n
    freqs = np.fft.rfftfreq(n)

    mask = freqs > 0
    freqs = freqs[mask]
    psd = psd[mask]

    # 🔥 بدون حذف bias
    log_f = np.log(freqs + 1e-12)
    log_psd = np.log(psd + 1e-12)

    # 🔥 robust fit بدل polyfit
    median_f = np.median(log_f)
    median_psd = np.median(log_psd)

    slope = np.sum((log_f - median_f)*(log_psd - median_psd)) / \
            np.sum((log_f - median_f)**2 + 1e-12)

    alpha = -slope

    return float(alpha)
