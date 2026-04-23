import numpy as np
import pandas as pd
from analysis.numerical_spectral_verification import estimate_alpha

DATASETS = {
    "sunspots": "real-data/sunspots_global.csv",
    "stock": "real-data/vix.csv",
    "synthetic_noise": None
}

def generate_noise(n=2000):
    return np.random.normal(0,1,n)

def load_series(path):
    df = pd.read_csv(path)

    for col in df.columns:
        if col.lower() in ["value","close"]:
            return df[col].dropna().values

    raise ValueError("No valid column found")

def run():
    results = {}

    for name, path in DATASETS.items():
        if path is None:
            series = generate_noise()
        else:
            series = load_series(path)

        alpha = estimate_alpha(series)
        results[name] = alpha
        print(f"{name}: {alpha}")

    return results


if __name__ == "__main__":
    res = run()

    values = list(res.values())
    spread = max(values) - min(values)

    print("Spread:", spread)

    if spread > 0.5:
        print("❌ COLLAPSE → not universal")
        exit(1)

    print("✅ UNIVERSAL STABILITY DETECTED")
