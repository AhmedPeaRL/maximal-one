import numpy as np

def estimate_alpha(series):
    series = np.asarray(series)
    series = series - np.mean(series)
    n = len(series)

    window = np.hanning(n)
    series = series * window

    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / n
    freqs = np.fft.rfftfreq(n)

    mask = (freqs > 0) & (freqs < 0.5)
    freqs = freqs[mask]
    psd = psd[mask]

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    # linear regression حقيقية
    A = np.vstack([log_f, np.ones(len(log_f))]).T
    slope, intercept = np.linalg.lstsq(A, log_psd, rcond=None)[0]

    alpha = -slope
    return float(alpha)
