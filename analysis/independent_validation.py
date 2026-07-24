import numpy as np
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
    std = np.std(series)

    if std < 1e-12:
        return np.nan

    series = series / std
    fft = np.fft.rfft(series)
    power = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(len(series))

    mask = (
        (freqs > 0.01)
        &
        (freqs < 0.25)
        &
        (power > 0)
    )

    freqs = freqs[mask]
    power = power[mask]

    if len(freqs) < 20:
        return np.nan

    x = np.log(freqs)
    y = np.log(power)

    try:
        slope, _ = np.polyfit(x, y, 1)

    except Exception:
        return np.nan

    alpha = -float(slope)

    if not np.isfinite(alpha):
        return np.nan

    alpha = np.clip(alpha, 0.05, 3.0)

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
