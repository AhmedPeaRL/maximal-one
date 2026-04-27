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

    # robust but sensitive fit
    weights = 1 / (1 + np.abs(log_psd - np.median(log_psd)))

    slope = np.sum(weights * (log_f - np.mean(log_f)) * (log_psd - np.mean(log_psd))) / \
           (np.sum(weights * (log_f - np.mean(log_f))**2) + 1e-12)
   
    alpha = -slope

    return float(alpha)
