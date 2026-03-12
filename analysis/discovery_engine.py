import json
import numpy as np
import pandas as pd
from glob import glob

OUTPUT = "artifacts/discovery_candidates.json"


def spectral_alpha(x):
    f = np.fft.rfft(x)
    power = np.abs(f)**2
    freqs = np.arange(len(power))

    mask = freqs > 0
    slope = np.polyfit(np.log(freqs[mask]), np.log(power[mask]), 1)[0]
    return slope


def entropy(x):
    hist,_ = np.histogram(x, bins=50, density=True)
    hist = hist[hist>0]
    return -np.sum(hist*np.log(hist))


def extract_features(series):

    return {
        "spectral_alpha": spectral_alpha(series),
        "entropy": entropy(series),
        "variance": float(np.var(series))
    }


def main():

    datasets = glob("real-data/*.csv")

    results = {}

    for d in datasets:

        df = pd.read_csv(d)
        s = df.iloc[:,1].values

        results[d] = extract_features(s)

    with open(OUTPUT,"w") as f:
        json.dump(results,f,indent=2)

    print(json.dumps(results,indent=2))


if __name__ == "__main__":
    main()
