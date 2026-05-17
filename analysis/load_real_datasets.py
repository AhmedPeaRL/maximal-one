import pandas as pd
import numpy as np
from pathlib import Path

DATASETS = {
    "sunspots": "real-data/sunspots_full.csv",
    "extended": "real-data/sunspots_global_extended.csv",
    "temperature": "real-data/temperature_global.csv",
    "sp500": "real-data/sp500.csv"
}

def load_series(path):

    if not Path(path).exists():
        raise ValueError(f"Missing file: {path}")

    df = pd.read_csv(path)

    # convert all to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(axis=1, how="all")

    for col in df.columns:
        series = df[col].dropna().values

        if len(series) < 200:
            continue

        std = np.std(series)
        if std < 1e-6:
            continue

        # normalize
        series = (series - np.mean(series)) / std

        return series

    raise ValueError(f"No valid numeric column in {path}")

def load_all():

    out = {}

    for name, path in DATASETS.items():
        try:
            out[name] = load_series(path)
            print(f"✅ Loaded: {name}")
        except Exception as e:
            print(f"❌ Failed: {name} ({e})")

    if len(out) < 2:
        raise SystemExit("❌ Not enough real datasets")

    return out
