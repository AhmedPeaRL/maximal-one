import numpy as np
import pandas as pd
from scipy.signal import welch
from pathlib import Path
import json

WINDOW = 512
STEP = 256

# =========================
# SAFE FREQUENCY BAND
# =========================
FREQ_MIN = 0.01
FREQ_MAX = 0.2


def spectral_alpha(x):

    f, Pxx = welch(x, nperseg=256)

    # remove zero freq
    mask = (f > FREQ_MIN) & (f < FREQ_MAX)

    f = f[mask]
    Pxx = Pxx[mask]

    # guard: not enough points
    if len(f) < 10:
        return None

    logf = np.log(f)
    logp = np.log(Pxx + 1e-12)

    slope, _ = np.polyfit(logf, logp, 1)

    alpha = -slope

    # HARD CLIP (physical sanity)
    if alpha < 0 or alpha > 3:
        return None

    return float(alpha)


def analyze_series(series):

    results = []

    for i in range(0, len(series) - WINDOW, STEP):

        window = series[i:i+WINDOW]

        alpha = spectral_alpha(window)

        if alpha is not None:
            results.append(alpha)

    return results


def main():

    data_dir = Path("real-data")

    out = {}

    for f in data_dir.glob("*_clean.csv"):

        df = pd.read_csv(f)

        col = df.columns[0]

        series = df[col].values

        if len(series) < WINDOW:
            continue

        res = analyze_series(series)

        if len(res) == 0:
            continue

        out[f.name] = {
            "alphas": res,
            "mean_alpha": float(np.mean(res)),
            "std_alpha": float(np.std(res)),
            "count": len(res)
        }

    Path("artifacts").mkdir(exist_ok=True)

    with open("artifacts/windowed_spectral.json","w") as fp:
        json.dump(out, fp, indent=2)


if __name__ == "__main__":
    main()
