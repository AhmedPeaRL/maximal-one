import json
import numpy as np
import pandas as pd
from glob import glob
import os

OUTPUT = "artifacts/discovery_candidates.json"


def spectral_alpha(x):

    if len(x) < 64:
        return None

    f = np.fft.rfft(x)
    power = np.abs(f) ** 2
    freqs = np.arange(len(power))

    mask = freqs > 0

    if np.sum(mask) < 10:
        return None

    slope = np.polyfit(
        np.log(freqs[mask]),
        np.log(power[mask] + 1e-12),
        1
    )[0]

    return float(slope)


def entropy_feature(x):

    hist, _ = np.histogram(x, bins=50, density=True)

    hist = hist[hist > 0]

    if len(hist) == 0:
        return None

    return float(-np.sum(hist * np.log(hist)))


def extract_features(series):

    alpha = spectral_alpha(series)

    ent = entropy_feature(series)

    var = float(np.var(series))

    return {
        "spectral_alpha": alpha,
        "entropy": ent,
        "variance": var
    }


def safe_read_csv(path):

    if os.path.getsize(path) == 0:
        print("Skipping empty file:", path)
        return None

    try:
        df = pd.read_csv(path)
    except Exception as e:
        print("CSV read error:", path, str(e))
        return None

    if df.shape[1] < 2:
        print("Skipping malformed dataset:", path)
        return None

    return df


def main():

    datasets = glob("real-data/*.csv")

    results = {}

    for d in datasets:

        df = safe_read_csv(d)

        if df is None:
            continue

        series = df.iloc[:, 1].values

        if len(series) < 100:
            print("Skipping short dataset:", d)
            continue

        features = extract_features(series)

        results[d] = features

        print("Processed:", d)

    os.makedirs("artifacts", exist_ok=True)

    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2)

    print("Discovery results saved.")


if __name__ == "__main__":
    main()
