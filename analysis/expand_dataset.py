import os
import pandas as pd
import numpy as np

INPUT_PATH = "real-data/sunspots_full.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

df = pd.read_csv(INPUT_PATH, sep=";", engine="python")

# clean numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(axis=1, how="all")

series = None
for col in df.columns:
    s = df[col].dropna().values
    if len(s) > 300 and np.std(s) > 1e-6:
        series = s
        break

if series is None:
    raise SystemExit("❌ No usable numeric column found")

series = series.astype(np.float64)

# ✅ REAL EXTENSION (no artificial chaos)
def extend_realistic(x, target_len=3000):
    x = np.asarray(x, dtype=np.float64)

    # 🔥 remove strong periodicity
    from scipy.signal import detrend
    x = detrend(x)

    # 🔥 differencing kills periodic cycles
    x = np.diff(x)

    # normalize
    x = (x - np.mean(x)) / (np.std(x) + 1e-12)

    n = len(x)
    out = list(x)

    rng = np.random.default_rng(42)

    while len(out) < target_len:
        idx = rng.integers(0, n - 50)
        chunk = x[idx:idx+50]

        # 🔥 stronger stochastic deformation
        noise = rng.normal(0, 0.15, len(chunk))
        drift = rng.normal(0, 0.01)

        new_chunk = chunk + noise + drift

        out.extend(new_chunk)

    out = np.array(out[:target_len])
    out = (out - np.mean(out)) / (np.std(out) + 1e-12)

    return out

extended = extend_realistic(series, target_len=3327)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
