import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.decomposition import PCA
import json

DATA_DIR = "real-data"
OUT = "artifacts/universality_manifold.json"


def spectral_alpha(x):

    x = x - np.mean(x)

    f = np.fft.rfft(x)
    psd = np.abs(f)**2

    freqs = np.fft.rfftfreq(len(x))

    mask = freqs > 0

    freqs = freqs[mask]
    psd = psd[mask]

    logf = np.log(freqs)
    logp = np.log(psd)

    slope = np.polyfit(logf, logp, 1)[0]

    return -slope


def hurst(x):

    N = len(x)

    T = np.arange(1, N+1)

    Y = np.cumsum(x - np.mean(x))

    R = np.maximum.accumulate(Y) - np.minimum.accumulate(Y)

    S = np.std(x)

    if S == 0:
        return np.nan

    return np.log(R[-1]/S) / np.log(N)


def entropy(x, bins=50):

    hist,_ = np.histogram(x, bins=bins, density=True)

    hist = hist[hist>0]

    return -np.sum(hist*np.log(hist))


def features(series):

    return [
        spectral_alpha(series),
        hurst(series),
        entropy(series)
    ]


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

            X.append(features(x))
            names.append(f.name)

        except Exception:
            pass

    X = np.array(X)

    pca = PCA(n_components=2)

    coords = pca.fit_transform(X)

    result = {
        "systems": names,
        "explained_variance": pca.explained_variance_ratio_.tolist(),
        "coordinates": coords.tolist()
    }

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    run()
