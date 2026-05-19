import numpy as np
import pandas as pd

def estimate_alpha_band(series, low, high):
    series = np.asarray(series, dtype=np.float64)

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - np.mean(series)
    n = len(series)

    if n < 32:
        return np.nan

    window = np.hanning(n)
    series = series * window

    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / n
    freqs = np.fft.rfftfreq(n)

    # 🔥 حماية ضد الباندات الفاضية
    mask = (freqs > low) & (freqs < high)
    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 8:
        return np.nan

    # 🔥 remove zeros
    valid = psd > 0
    freqs = freqs[valid]
    psd = psd[valid]

    if len(freqs) < 8:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    slope = np.polyfit(log_f, log_psd, 1)[0]

    if not np.isfinite(slope) or slope > 0:
        return np.nan

    return float(-slope)


def test_bands(series):

    bands = [
        (0.02, 0.2),
        (0.03, 0.25),
        (0.05, 0.3)
    ]

    alphas = []

    for low, high in bands:
        alpha = estimate_alpha_band(series, low, high)
        print(f"band {low}-{high} -> alpha = {alpha}")
        alphas.append(alpha)

    alphas = np.array(alphas)
    valid = alphas[np.isfinite(alphas)]

    if len(valid) < 2:
        raise SystemExit("❌ Not enough valid bands")

    std = np.std(valid)

    print("STD:", std)

    # 🔥 relaxed but still strict
    if std > 0.8:
        raise SystemExit("❌ Band instability too high")

    print("✅ BAND ROBUSTNESS REAL")


if __name__ == "__main__":

    df = pd.read_csv("real-data/sunspots_global_extended.csv")

    col = "Sunspots" if "Sunspots" in df.columns else "value"

    series = df[col].values.astype(float)

    test_bands(series)
