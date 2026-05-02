import numpy as np
from scipy.signal import welch
from scipy.stats import linregress

def estimate_alpha_welch(series):
    series = np.asarray(series)
    series = series - np.mean(series)

    freqs, psd = welch(series, nperseg=min(256, len(series)))

    mask = (freqs > 0.02) & (freqs < 0.25)
    freqs = freqs[mask]
    psd = psd[mask]

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-10)

    slope, _, _, _, _ = linregress(log_f, log_psd)

    return -slope


def compare_methods(series):
    from analysis.numerical_spectral_verification import estimate_alpha

    a1 = estimate_alpha(series)
    a2 = estimate_alpha_welch(series)

    print("Method 1 (FFT median slope):", a1)
    print("Method 2 (Welch):", a2)

    if abs(a1 - a2) > 0.5:
        return "unstable/adversarial"
    else:
        return "valid structure"

    print("✅ Independent methods agree")
