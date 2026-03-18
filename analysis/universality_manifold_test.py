import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.decomposition import PCA
import json

DATA_DIR = "real-data"
OUT = "artifacts/universality_manifold.json"


EPS = 1e-12


def safe_log(x):
    return np.log(np.clip(x, EPS, None))


def spectral_alpha(x):

    x = x - np.mean(x)

    f = np.fft.rfft(x)
    psd = np.abs(f)**2

    freqs = np.fft.rfftfreq(len(x))

    mask = freqs > 0

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 10:
        return np.nan

    logf = safe_log(freqs)
    logp = safe_log(psd)

    if np.any(~np.isfinite(logf)) or np.any(~np.isfinite(logp)):
        return np.nan

    slope = np.polyfit(logf, logp, 1)[0]

    return -slope


def hurst(x):

    N = len(x)

    if N < 50:
        return np.nan

    Y = np.cumsum(x - np.mean(x))

    R = np.max(Y) - np.min(Y)

    S = np.std(x)

    if S < EPS or R < EPS:
        return np.nan

    return np.log(R / S) / np.log(N)


def entropy(x, bins=50):

    hist, _ = np.histogram(x, bins=bins, density=True)

    hist = hist[hist > 0]

    if len(hist) < 5:
        return np.nan

    return -np.sum(hist * np.log(hist))


def features(series):

    f = [
        spectral_alpha(series),
        hurst(series),
        entropy(series)
    ]

    return np.array(f, dtype=float)


def run():

    X = []
    names = []

    for f in Path(DATA_DIR).glob("*.csv"):

        try:
            df = pd.read_csv(f)

            col = df.columns[0]

            x = df[col].dropna().values

            if len(x) < 300:
                continue

            feat = features(x)

            if np.any(~np.isfinite(feat)):
                continue

            X.append(feat)
            names.append(f.name)

        except Exception:
            continue

    if len(X) < 3:
        result = {
            "error": "not enough valid systems",
            "n_valid": len(X)
        }

        Path("artifacts").mkdir(exist_ok=True)
        with open(OUT, "w") as f:
            json.dump(result, f, indent=2)

        print(result)
        return

    X = np.array(X)

    # normalization (مهم جدًا)
    X = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + EPS)

    pca = PCA(n_components=2)

    coords = pca.fit_transform(X)

    result = {
        "systems": names,
        "explained_variance": pca.explained_variance_ratio_.tolist(),
        "coordinates": coords.tolist(),
        "n_systems": len(names)
    }

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
