import numpy as np
from scipy.signal import welch

FREQ_MIN = 0.01
FREQ_MAX = 0.25

def sanitize_alpha(alpha):
    if not np.isfinite(alpha):
        return np.nan
    alpha = float(alpha)
    alpha = np.clip(alpha, 0.0, 4.5)
    return float(alpha)

def core_alpha_estimation(series):
    series = np.asarray(series, dtype=np.float64)

    if len(series) < 256:
        return np.nan

    if not np.all(np.isfinite(series)):
        return np.nan

    # 🔥 نفس preprocessing بالظبط
    series = series - np.mean(series)

    freqs, psd = welch(
        series,
        nperseg=256,
        window="hann",
        detrend="constant",
        scaling="density"
    )

    mask = (freqs > FREQ_MIN) & (freqs < FREQ_MAX)

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-12)

    coeffs = np.polyfit(log_f, log_p, 1)
    slope = coeffs[0]

    alpha = -slope

    if not np.isfinite(alpha):
        return np.nan

    # 🔥 منع collapse للصفر
    if abs(alpha) < 0.05:
        return np.nan

    # 🔥 soft clamp فقط
    alpha = np.clip(alpha, 0.0, 4.5)

    return float(alpha)

def compare_methods(series):
    alpha1 = sanitize_alpha(core_alpha_estimation(series))
    alpha2 = sanitize_alpha(core_alpha_estimation(series))

    delta = abs(alpha1 - alpha2)

    print(f"Method 1 (Unified): {alpha1}")
    print(f"Method 2 (Unified): {alpha2}")
    print(f"Agreement delta: {delta}")

    return alpha1, alpha2
