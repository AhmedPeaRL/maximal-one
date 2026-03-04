import numpy as np

def generate_white_noise(n=4096, seed=42):
    rng = np.random.default_rng(seed)
    return rng.standard_normal(n)

def estimate_alpha(signal):
    # Power spectral density slope estimation (log-log fit)
    freqs = np.fft.rfftfreq(len(signal))
    psd = np.abs(np.fft.rfft(signal))**2

    # Remove zero frequency
    freqs = freqs[1:]
    psd = psd[1:]

    log_f = np.log(freqs)
    log_p = np.log(psd)

    slope, _ = np.polyfit(log_f, log_p, 1)
    alpha = -slope

    return alpha
