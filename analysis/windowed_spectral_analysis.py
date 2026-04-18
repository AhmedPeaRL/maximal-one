import numpy as np
import pandas as pd
from scipy.signal import welch
from pathlib import Path
import json

WINDOW = 512
STEP = 256

def spectral_alpha(x):

f, Pxx = welch(x, nperseg=256)

mask = (f > 0.01) & (f < 0.5)  # band selection مهم جداً
f = f[mask]
Pxx = Pxx[mask]

logf = np.log(f)
logp = np.log(Pxx)

# robust fit بدل polyfit العادي
slope = np.median(np.diff(logp) / np.diff(logf))

return -slope

def bootstrap_alpha(series, n=50):
estimates = []
for _ in range(n):
noise = np.random.normal(0, 0.01, len(series))
estimates.append(spectral_alpha(series + noise))
return np.mean(estimates), np.std(estimates)

def analyze_series(series):

results = []

for i in range(0, len(series) - WINDOW, STEP):

    window = series[i:i+WINDOW]

    alpha, sigma = bootstrap_alpha(window)

    results.append({
        "alpha": float(alpha),
        "sigma": float(sigma)
    })

return results

def main():

data_dir = Path("real-data")

out = {}

for f in data_dir.glob("*_clean.csv"):

    df = pd.read_csv(f)

    col = df.columns[0]

    series = df[col].values

    if len(series) < WINDOW:
        continue

    out[f.name] = analyze_series(series)

Path("artifacts").mkdir(exist_ok=True)

with open("artifacts/windowed_spectral.json","w") as fp:
    json.dump(out,fp, indent=2)

if name == "main":
main()
