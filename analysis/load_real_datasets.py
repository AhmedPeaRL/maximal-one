import pandas as pd
import numpy as np
from pathlib import Path

DATASETS = {
    "sunspots": "real-data/sunspots_full.csv",
    "co2": "real-data/co2_atmospheric_clean.csv",
    "passengers": "real-data/airline_passengers.csv",
    "cosmic_rays": "real-data/cosmic_rays_clean.csv",
    "extended": "real-data/sunspots_global_extended.csv",
    "temperature": "real-data/temperature_global.csv",
    "sp500": "real-data/sp500.csv"
}

def load_series(path):
    if not Path(path).exists():
        raise ValueError(f"Missing file: {path}")

    df = pd.read_csv(path, sep=None, engine="python", na_values=["***"], skiprows=1)

    best_series = None
    best_score = 0

    for col in df.columns:
        if "date" in col.lower() or "month" in col.lower():
            continue

        if col.lower() in ["passengers", "value"]:
            s = pd.to_numeric(df[col], errors="coerce")
        
        s = pd.to_numeric(df[col], errors="coerce").dropna().values

        if len(s) < 200:
            continue

        std = np.std(s)
        if std < 1e-6:
            continue

        score = std * len(s)

        if score > best_score:
            best_score = score
            best_series = s

    if best_series is None:
        raise ValueError(f"No valid numeric column in {path}")

    best_series = (best_series - np.mean(best_series)) / (np.std(best_series) + 1e-12)

    return best_series


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
