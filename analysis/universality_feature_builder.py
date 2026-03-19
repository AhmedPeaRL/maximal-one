import os
import json
import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import entropy

DATA_DIR = "real-data"


def spectral_alpha(x):
    f, Pxx = welch(x, nperseg=min(256, len(x)))
    f = f[1:]
    Pxx = Pxx[1:]

    if len(f) < 5:
        return None

    logf = np.log(f)
    logp = np.log(Pxx + 1e-12)

    slope = np.polyfit(logf, logp, 1)[0]

    return float(-slope)


def hurst(ts):
    if len(ts) < 50:
        return None

    lags = range(2, 20)
    tau = [np.std(ts[lag:] - ts[:-lag]) for lag in lags]
    tau = np.array(tau)

    if np.any(tau <= 0):
        return None

    poly = np.polyfit(np.log(list(lags)), np.log(tau), 1)

    return float(poly[0] * 2.0)


def entropy_rate(x, bins=50):
    hist, _ = np.histogram(x, bins=bins, density=True)
    hist = hist[hist > 0]

    if len(hist) == 0:
        return None

    return float(entropy(hist))


def attractor_dimension(x, m=5):
    x = np.array(x)

    if len(x) < 300:
        return None

    N = len(x)

    try:
        emb = np.column_stack([x[i:N - m + i] for i in range(m)])
    except Exception:
        return None

    if emb.shape[0] < 50:
        return None

    emb = emb[np.isfinite(emb).all(axis=1)]

    if len(emb) < 50:
        return None

    MAX_POINTS = 2000

    if len(emb) > MAX_POINTS:
        idx = np.random.choice(len(emb), MAX_POINTS, replace=False)
        emb = emb[idx]

    diff = emb[:, None, :] - emb[None, :, :]
    sq = (diff ** 2).sum(axis=-1)
    sq = sq[np.isfinite(sq)]
    sq = sq[sq >= 0]

    if len(sq) < 10:
        return None

    sq = np.clip(sq, 0, None)
    dists = np.sqrt(sq)
    dists = dists[np.isfinite(dists)]

    if len(dists) < 10:
        return None

    r = np.percentile(dists, 5)

    if r <= 0:
        return None

    C = np.mean(dists < r)

    if C <= 0:
        return None

    return float(-np.log(C) / np.log(r + 1e-9))


def load_series(path):
    try:
        df = pd.read_csv(path)
    except:
        return None

    if df.empty:
        return None

    for col in df.columns:
        if np.issubdtype(df[col].dtype, np.number):
            series = df[col].dropna().values
            if len(series) > 100:
                return series

    return None


features = []

if os.path.isdir(DATA_DIR):

    for f in os.listdir(DATA_DIR):

        if not f.endswith(".csv"):
            continue

        path = os.path.join(DATA_DIR, f)

        ts = load_series(path)

        if ts is None:
            print("Skipping invalid dataset:", f)
            continue

        dataset_name = f.replace(".csv", "")

        try:
            alpha = spectral_alpha(ts)
            ent = entropy_rate(ts)
            h = hurst(ts)
            dim = attractor_dimension(ts)

            values = [v for v in [alpha, ent, h] if v is not None]

            variance = float(np.var(values)) if values else None

            feat = {
                "name": f"{dataset_name}_signature",
                "dataset": dataset_name,
                "spectral_alpha": alpha,
                "entropy_rate": ent,
                "hurst_exponent": h,
                "attractor_dimension": dim,
                "variance": variance
            }

            features.append(feat)

        except Exception as e:
            print("Feature extraction failed:", f, str(e))


os.makedirs("artifacts", exist_ok=True)

with open("artifacts/universality_features.json", "w") as f:
    json.dump(features, f, indent=2)

pd.DataFrame(features).to_csv("artifacts/universality_features.csv", index=False)

print("Datasets processed:", len(features))
print("Features saved.")
