import os
import json
import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import entropy

DATA_DIR = "real-data"
OUT = "artifacts/invariant_scan.json"

def spectral_alpha(x):
    f, Pxx = welch(x, nperseg=min(256,len(x)))
    f = f[1:]
    Pxx = Pxx[1:]
    logf = np.log(f)
    logP = np.log(Pxx)
    a, b = np.polyfit(logf, logP, 1)
    return -a

def entropy_slope(x):
    bins = np.histogram(x, bins=50)[0] + 1e-9
    H = entropy(bins)
    return float(H)

def attractor_dim(x):
    N = len(x)
    r = np.std(x) * 0.2
    count = 0
    for i in range(N):
        for j in range(i+1,N):
            if abs(x[i]-x[j]) < r:
                count += 1
    C = count / (N*(N-1)/2)
    if C <= 0:
        return 0
    return -np.log(C)/np.log(r)

def load_series(path):
    df = pd.read_csv(path)
    for c in df.columns:
        if df[c].dtype != object:
            return df[c].dropna().values
    return None

results = []

for f in os.listdir(DATA_DIR):
    if not f.endswith(".csv"):
        continue
    path = os.path.join(DATA_DIR,f)
    x = load_series(path)
    if x is None or len(x)<200:
        continue

    x = (x - np.mean(x)) / np.std(x)

    try:
        res = {
            "dataset":f,
            "spectral_alpha":float(spectral_alpha(x)),
            "entropy":float(entropy_slope(x)),
            "attractor_dim":float(attractor_dim(x))
        }
        results.append(res)
    except Exception as e:
        print("skip",f,e)

os.makedirs("artifacts",exist_ok=True)

with open(OUT,"w") as g:
    json.dump(results,g,indent=2)

print(json.dumps(results,indent=2))
