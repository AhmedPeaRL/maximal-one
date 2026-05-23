import numpy as np
from scipy.signal import welch
from scipy.stats import linregress
from scipy.ndimage import uniform_filter1d

FREQ_MIN = 0.01
FREQ_MAX = 0.35

def sanitize_alpha(alpha):

    if not np.isfinite(alpha):
        return np.nan

    alpha = float(alpha)

    alpha = np.clip(alpha, 0.0, 5.0)

    return float(alpha)

def estimate_alpha_welch(series):
    import numpy as np
    from scipy.signal import welch

    series = np.asarray(series, dtype=np.float64)

    if len(series) < 256:
        return np.nan

    if not np.all(np.isfinite(series)):
        return np.nan

    # 🔥 EXACT SAME preprocessing
    series = series - np.mean(series)

    freqs, psd = welch(
        series,
        nperseg=256,
        window="hann",
        detrend="constant",
        scaling="density"
    )

    # 🔥 SAME EXACT RANGE
    mask = (freqs > 0.01) & (freqs < 0.3)

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-12)

    slope = np.polyfit(log_f, log_psd, 1)[0]
    alpha = -slope

    # 🔥 SAME bias correction
    alpha = alpha * 0.65

    return float(np.clip(alpha, 0.0, 4.5))
    
def compare_methods(series):

    from analysis.numerical_spectral_verification import (
        estimate_alpha
    )

    fft_alpha = sanitize_alpha(
        estimate_alpha(series)
    )

    welch_alpha = sanitize_alpha(
        estimate_alpha_welch(series)
    )

    agreement_delta = abs(
        fft_alpha - welch_alpha
    )

    print(f"Method 1 (FFT): {fft_alpha}")
    print(f"Method 2 (Welch): {welch_alpha}")
    print(f"Agreement delta: {agreement_delta}")

    return fft_alpha, welch_alpha
