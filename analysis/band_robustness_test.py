import numpy as np
import pandas as pd

def estimate_alpha_band(series, low, high):
    series = np.asarray(series)
    series = series - np.mean(series)
    n = len(series)

    window = np.hanning(n)
    series = series * window

    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / n
    freqs = np.fft.rfftfreq(n)

    mask = (freqs > low) & (freqs < high)
    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 10:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd + 1e-10)

    slope = np.polyfit(log_f, log_psd, 1)[0]

    return float(-slope)


def test_bands(series):

    bands = [
        (0.01, 0.1),
        (0.02, 0.25),
        (0.05, 0.3),
        (0.01, 0.4)
    ]

    alphas = []

    for low, high in bands:
        alpha = estimate_alpha_band(series, low, high)
        print(f"band {low}-{high} -> alpha = {alpha}")
        alphas.append(alpha)

    std = np.nanstd(alphas)

    if std > 0.4:
        raise SystemExit("❌ Band instability too high")

    print("✅ BAND ROBUSTNESS REAL")


if __name__ == "__main__":

    df = pd.read_csv("real-data/sunspots_global.csv")

    col = "Sunspots" if "Sunspots" in df.columns else "value"

    series = df[col].values.astype(float)

    test_bands(series)
