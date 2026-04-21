import numpy as np

def estimate_alpha(series):
    """
    Proper spectral alpha estimation using PSD
    """

    # Remove mean
    series = series - np.mean(series)

    # FFT
    fft_vals = np.fft.rfft(series)
    psd = np.abs(fft_vals) ** 2

    freqs = np.fft.rfftfreq(len(series))

    # Remove zero freq
    mask = freqs > 0
    freqs = freqs[mask]
    psd = psd[mask]

    # Log-log fit
    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-12)

    slope, _ = np.polyfit(log_f, log_psd, 1)

    alpha = -slope

    return float(alpha)
