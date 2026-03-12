import json
import numpy as np
import pandas as pd
from glob import glob
from pathlib import Path

OUT = "artifacts/universal_invariants.json"


def spectral_alpha(x):

    f = np.fft.rfft(x - np.mean(x))

    p = np.abs(f)**2

    freqs = np.fft.rfftfreq(len(x))

    mask = freqs > 0

    logf = np.log(freqs[mask])
    logp = np.log(p[mask])

    slope = np.polyfit(logf,logp,1)[0]

    return float(-slope)


def entropy(x):

    hist,_ = np.histogram(x,bins=64,density=True)

    hist = hist[hist>0]

    return float(-np.sum(hist*np.log(hist)))


def attractor_dim(x):

    diff = np.abs(x[:-1]-x[1:])

    eps = np.std(diff)

    c = np.sum(diff < eps)/len(diff)

    if c<=0:
        return None

    return float(np.log(c)/np.log(eps))


def load_series(path):

    df = pd.read_csv(path)

    numeric = df.select_dtypes(include=[np.number])

    if numeric.shape[1]==0:
        return None

    s = numeric.iloc[:,0].dropna()

    if len(s) < 200:
        return None

    return s.values


def main():

    datasets = glob("real-data/*.csv")

    results = []

    for path in datasets:

        try:

            x = load_series(path)

            if x is None:
                continue

            r = {
                "dataset":Path(path).name,
                "spectral_alpha":spectral_alpha(x),
                "entropy":entropy(x),
                "attractor_dim":attractor_dim(x)
            }

            results.append(r)

            print("scanned",path)

        except Exception as e:

            print("skip",path,str(e))

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:

        json.dump(results,f,indent=2)

    print("Universal scan complete")


if __name__ == "__main__":
    main()
