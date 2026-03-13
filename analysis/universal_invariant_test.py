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

    if len(f) < 5:
        return None

    logf = np.log(f)
    logp = np.log(Pxx + 1e-12)

    a, b = np.polyfit(logf, logp, 1)
    return float(-a)


def entropy_slope(x):
    hist,_ = np.histogram(x, bins=50, density=True)
    hist += 1e-12
    return float(entropy(hist))


def attractor_dimension(x):
    x = (x - np.mean(x)) / (np.std(x)+1e-12)
    return float(np.var(np.diff(x)))


results = {}

if not os.path.exists(DATA_DIR):
    print("Dataset directory missing")
    exit(0)

for file in os.listdir(DATA_DIR):

    if not file.endswith(".csv"):
        continue

    path = os.path.join(DATA_DIR, file)

    # Skip empty files
    if os.path.getsize(path) == 0:
        print(f"Skipping empty file: {file}")
        continue

    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"Skipping unreadable file {file}: {e}")
        continue

    if df.empty:
        print(f"Skipping dataframe with no rows: {file}")
        continue

    numeric_cols = df.select_dtypes(include=[np.number])

    if numeric_cols.shape[1] == 0:
        print(f"No numeric columns in {file}")
        continue

    series = numeric_cols.iloc[:,0].dropna().values

    if len(series) < 200:
        print(f"Series too short in {file}")
        continue

    try:
        results[file] = {
            "spectral_alpha": spectral_alpha(series),
            "entropy": entropy_slope(series),
            "dimension_proxy": attractor_dimension(series)
        }
    except Exception as e:
        print(f"Computation failed for {file}: {e}")

os.makedirs("artifacts", exist_ok=True)

with open(OUT,"w") as f:
    json.dump(results,f,indent=2)

print(json.dumps(results,indent=2))
