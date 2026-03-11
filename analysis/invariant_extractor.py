import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import entropy
import json
import os

def spectral_alpha(x):

    f, p = welch(x, nperseg=256)

    logf = np.log(f[1:])
    logp = np.log(p[1:])

    alpha = np.polyfit(logf, logp, 1)[0]

    return float(alpha)

def entropy_slope(x):

    hist,_ = np.histogram(x, bins=50)
    e = entropy(hist)

    return float(e)

def attractor_dimension(x):

    return float(np.log(len(x)) / np.log(2))

def analyze_dataset(path):

    df = pd.read_csv(path)

    series = df.iloc[:,1].values

    result = {
        "dataset": os.path.basename(path),
        "spectral_alpha": spectral_alpha(series),
        "entropy": entropy_slope(series),
        "dimension": attractor_dimension(series)
    }

    return result

def main():

    results = []

    for f in os.listdir("real-data"):
        if f.endswith(".csv"):
            r = analyze_dataset("real-data/"+f)
            results.append(r)

    os.makedirs("artifacts",exist_ok=True)

    with open("artifacts/invariants.json","w") as f:
        json.dump(results,f,indent=2)

if __name__ == "__main__":
    main()
