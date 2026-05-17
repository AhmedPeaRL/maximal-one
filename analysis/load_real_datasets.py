import pandas as pd
import numpy as np
from pathlib import Path

DATASETS = {
    "sunspots": "real-data/sunspots_full.csv",
    "temperature": "real-data/temperature_global.csv",
    "sp500": "real-data/sp500.csv"
}

def load_series(path):

    df = pd.read_csv(path)

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            series = df[col].dropna().values

            if len(series) < 200:
                raise ValueError(f"Too small: {path}")

            std = np.std(series)
            if std < 1e-6:
                raise ValueError(f"Constant series: {path}")

            series = (series - np.mean(series)) / std

            return series

    raise ValueError(f"No numeric column: {path}")


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
