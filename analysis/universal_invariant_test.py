import os
import json
import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import entropy

DATA_DIR = "real-data"
OUT = "artifacts/universal_invariant_test.json"

def spectral_alpha(x):
    f, Pxx = welch(x, nperseg=min(256, len(x)))
    f = f[1:]
    Pxx = Pxx[1:]
    logf = np.log(f)
    logp = np.log(Pxx)
    a, b = np.polyfit(logf, logp, 1)
    return -a

def entropy_slope(x):
    hist,_ = np.histogram(x, bins=50, density=True)
    hist += 1e-12
    return entropy(hist)

def attractor_dimension(x):
    x = (x - np.mean(x)) / (np.std(x)+1e-12)
    return np.var(np.diff(x))

results = {}

for file in os.listdir(DATA_DIR):
    if not file.endswith(".csv"):
        continue

    path = os.path.join(DATA_DIR, file)
    df = pd.read_csv(path)

    series = df.select_dtypes(include=[np.number]).iloc[:,0].dropna().values

    if len(series) < 200:
        continue

    results[file] = {
        "spectral_alpha": float(spectral_alpha(series)),
        "entropy": float(entropy_slope(series)),
        "dimension_proxy": float(attractor_dimension(series))
    }

os.makedirs("artifacts", exist_ok=True)

with open(OUT,"w") as f:
    json.dump(results,f,indent=2)

print(json.dumps(results,indent=2))
