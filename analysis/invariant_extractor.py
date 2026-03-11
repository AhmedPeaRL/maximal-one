import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import entropy
import json
import os

def spectral_alpha(x):

    if len(x) < 10:
        return None

    f, p = welch(x, nperseg=min(256,len(x)))

    f = f[1:]
    p = p[1:]

    if len(f) == 0 or len(p) == 0:
        return None

    logf = np.log(f)
    logp = np.log(p)

    alpha = np.polyfit(logf, logp, 1)[0]

    return float(alpha)


def entropy_slope(x):

    if len(x) < 10:
        return None

    hist,_ = np.histogram(x, bins=50)

    if hist.sum() == 0:
        return None

    e = entropy(hist)

    return float(e)


def attractor_dimension(x):

    if len(x) < 10:
        return None

    return float(np.log(len(x)) / np.log(2))


def load_series(df):

    # حاول العثور على أول عمود رقمي
    for col in df.columns:
        try:
            series = pd.to_numeric(df[col], errors='coerce').dropna()
            if len(series) > 10:
                return series.values
        except:
            pass

    return None


def analyze_dataset(path):

    try:

        if os.path.getsize(path) == 0:
            print("Empty file:", path)
            return None

        df = pd.read_csv(path)

        if df.shape[0] == 0:
            print("No rows:", path)
            return None

        series = load_series(df)

        if series is None:
            print("No numeric column:", path)
            return None

        result = {
            "dataset": os.path.basename(path),
            "spectral_alpha": spectral_alpha(series),
            "entropy": entropy_slope(series),
            "dimension": attractor_dimension(series)
        }

        return result

    except Exception as e:

        print("Dataset skipped:", path, "error:", str(e))

        return None


def main():

    results = []

    if not os.path.exists("real-data"):
        print("real-data folder missing")
        return

    for f in os.listdir("real-data"):

        if not f.endswith(".csv"):
            continue

        path = os.path.join("real-data",f)

        r = analyze_dataset(path)

        if r is not None:
            results.append(r)

    os.makedirs("artifacts",exist_ok=True)

    with open("artifacts/invariants.json","w") as f:
        json.dump(results,f,indent=2)

    print("Extracted invariants from",len(results),"datasets")


if __name__ == "__main__":
    main()
