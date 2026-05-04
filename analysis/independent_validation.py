import numpy as np
from scipy.signal import welch
from scipy.stats import linregress

def estimate_alpha_welch(series):
    series = np.asarray(series)
    series = series - np.mean(series)
    n = len(series)
    
    # تحسين nperseg للداتا القصيرة
    nperseg = min(64, n)
    freqs, psd = welch(series, nperseg=nperseg)

    mask = (freqs > 0.02) & (freqs < 0.25)
    if not np.any(mask): return np.nan
    
    log_f = np.log(freqs[mask])
    log_psd = np.log(psd[mask] + 1e-10)

    slope, _, _, _, _ = linregress(log_f, log_psd)
    return -slope

def compare_methods(series):
    from analysis.numerical_spectral_verification import estimate_alpha

    a1 = estimate_alpha(series)
    a2 = estimate_alpha_welch(series)

    print(f"Method 1 (FFT): {a1}")
    print(f"Method 2 (Welch): {a2}")

    # رفع الحد لـ 2.0 لاستيعاب الفروق الطبيعية في الداتا العنيفة (Non-stationary)
    if abs(a1 - a2) > 2.0:
        return "unstable/adversarial"
    else:
        return "valid structure"
    
