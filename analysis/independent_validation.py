import numpy as np
from scipy.signal import welch

from analysis.numerical_spectral_verification import estimate_alpha

FREQ_MIN = 0.01
FREQ_MAX = 0.25


def sanitize_alpha(alpha):
    if alpha is None:
        return np.nan

    if not np.isfinite(alpha):
        return np.nan

    alpha = float(alpha)

    # 🔥 consistent with strict_claim
    alpha = np.clip(alpha, 0.0, 4.5)

    return float(alpha)


def core_alpha_estimation(series):
    series = np.asarray(series, dtype=np.float64)

    if len(series) < 256:
        return np.nan

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - np.mean(series)

    # 🔥 scale without killing structure
    std = np.std(series)
    if std > 1e-6:
        series = series / std

    freqs, psd = welch(
        series,
        nperseg=256,
        window="hann",
        detrend="linear",
        scaling="density"
    )

    mask = (freqs > FREQ_MIN) & (freqs < FREQ_MAX)

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-12)

    try:
        coeffs = np.polyfit(log_f, log_psd, 1)
        slope = coeffs[0]
    except Exception:
        return np.nan

    alpha = -slope

    if not np.isfinite(alpha):
        return np.nan

    # 🔥 collapse guard
    if abs(alpha) < 0.05:
        return np.nan

    alpha = np.clip(alpha, 0.0, 4.5)

    return float(alpha)


def compare_methods(series):
    """
    🔥 TRUE independent validation:
    - Method 1: estimate_alpha (robust FFT pipeline)
    - Method 2: Welch regression
    """

    alpha_fft = sanitize_alpha(
        estimate_alpha(series)
    )

    alpha_welch = sanitize_alpha(
        core_alpha_estimation(series)
    )

    if not (np.isfinite(alpha_fft) and np.isfinite(alpha_welch)):
        print("⚠️ invalid alpha in one method")
        return alpha_fft, alpha_welch

    delta = abs(alpha_fft - alpha_welch)

    print(f"FFT alpha: {alpha_fft}")
    print(f"Welch alpha: {alpha_welch}")
    print(f"Agreement delta: {delta}")

    return alpha_fft, alpha_welch
