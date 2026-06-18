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

    df = pd.read_csv(
        path,
        sep=None,
        engine="python",
        quoting=3,
        on_bad_lines="skip"
    )
    df.columns = [str(c).strip().lower() for c in df.columns]

    # 🔥🔥 FIX حقيقي للـ SP500 (قبل أي loop)
    if "sp500" in path.lower():
        for col in df.columns:
            col_lower = col.lower()
            if "close" in col_lower:
                s = pd.to_numeric(df[col], errors="coerce")
                s = s.replace([np.inf, -np.inf], np.nan).dropna()

                if len(s) > 120:
                    return (s - np.mean(s)) / (np.std(s) + 1e-12)

    if "temperature" in path.lower():
        df = pd.read_csv(path, skiprows=1, sep=",")
        df.columns = [c.strip() for c in df.columns]
        df = df.replace("***", np.nan)
        if "J-D" in df.columns:
            s = pd.to_numeric(df["J-D"], errors="coerce").dropna()
            if len(s) > 100:
                return (s - np.mean(s)) / (np.std(s) + 1e-12)

    best_series = None
    best_score = 0

    for col in df.columns:
        col_lower = col.lower()

        # 🔥 تجاهل الأعمدة الزمنية
        if any(x in col_lower for x in ["date", "month", "year"]):
            continue

        try:
            float(str(df[col].iloc[0]).replace(",", "").replace(" ", ""))
        except:
            continue

        df = df.replace("***", np.nan)
        s = pd.to_numeric(df[col], errors="coerce")
        s = s.replace([np.inf, -np.inf], np.nan)
        s = s.dropna()
        s = s[np.isfinite(s)]

        if len(s) < 80:
            continue

        std = np.std(s)
        if std < 1e-6:
            continue

        score = std * len(s)
        if score > best_score:
            best_score = score
            best_series = s

        df = df.replace(",", "", regex=True)

        # 🔥 passengers override
        if "passengers" in col_lower:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(s) > 100:
                return (s - np.mean(s)) / (np.std(s) + 1e-12)
    
    if best_series is None:
        raise ValueError(f"No valid numeric column in {path}")

    best_series = (best_series - np.mean(best_series)) / (np.std(best_series) + 1e-12)

    if len(best_series) < 256:
        best_series = np.pad(
            best_series,
            (0, 256 - len(best_series)),
            mode="reflect"
        )
    
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
        print("⚠️ Weak dataset loading — continuing with partial domain")
 
    return out
