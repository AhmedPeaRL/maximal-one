import os
import json
import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import entropy

DATA_DIR = "real-data"
OUT_PATH = "artifacts/universality_features.json"

def spectral_alpha(x):
    f, Pxx = welch(x, nperseg=min(256,len(x)))
    f = f[1:]
    Pxx = Pxx[1:]
    logf = np.log(f)
    logp = np.log(Pxx)
    slope = np.polyfit(logf, logp, 1)[0]
    return -slope

def hurst(ts):
    lags = range(2,20)
    tau = [np.std(np.subtract(ts[lag:],ts[:-lag])) for lag in lags]
    poly = np.polyfit(np.log(lags),np.log(tau),1)
    return poly[0]*2.0

def entropy_rate(x,bins=50):
    hist,_ = np.histogram(x,bins=bins,density=True)
    hist = hist[hist>0]
    return entropy(hist)

def attractor_dimension(x,m=5):
    N=len(x)
    if N<200:
        return None
    emb = np.column_stack([x[i:N-m+i] for i in range(m)])
    dists = np.sqrt(((emb[:,None]-emb[None,:])**2).sum(-1))
    r = np.percentile(dists,5)
    C = np.mean(dists<r)
    if C<=0:
        return None
    return -np.log(C)/np.log(r+1e-9)

def load_series(path):
    df=pd.read_csv(path)
    for col in df.columns:
        if np.issubdtype(df[col].dtype,np.number):
            return df[col].dropna().values
    return None

features=[]

if os.path.isdir(DATA_DIR):
    for f in os.listdir(DATA_DIR):
        if not f.endswith(".csv"):
            continue
        path=os.path.join(DATA_DIR,f)
        ts=load_series(path)
        if ts is None or len(ts)<200:
            continue
        try:
            feat={
                "dataset":f,
                "spectral_alpha":float(spectral_alpha(ts)),
                "entropy_rate":float(entropy_rate(ts)),
                "hurst_exponent":float(hurst(ts)),
                "attractor_dimension":float(attractor_dimension(ts))
            }
            features.append(feat)
        except Exception:
            continue

os.makedirs("artifacts",exist_ok=True)

with open(OUT_PATH,"w") as f:
    json.dump(features,f,indent=2)

print("Extracted features:",len(features))
