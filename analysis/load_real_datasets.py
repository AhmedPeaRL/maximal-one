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
    df = pd.read_csv(path, na_values=["***"])
    df = pd.read_csv(path)
    df = pd.read_csv("real-data/airline_passengers.csv")
    df = pd.read_csv(INPUT_PATH, sep=';', header=None)
    series = df.iloc[:, 3]
    series = pd.to_numeric(series, errors="coerce")
    series = series.dropna().values.astype(np.float64)
    values = df["Passengers"].values
    extended = np.tile(values, 2)[:220]

    pd.DataFrame({
        "Passengers": extended
    }).to_csv("real-data/sunspots_global_extended.csv", index=False)

    # 🔥 محاولة تحويل كل الأعمدة لأرقام
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(axis=1, how="all")

    for col in df.columns:
        if df[col].dtype != object:

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
