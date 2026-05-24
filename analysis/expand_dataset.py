import os
import pandas as pd
import numpy as np

INPUT_PATH = "real-data/sunspots_full.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

df = pd.read_csv(INPUT_PATH, sep=";", engine="python")

# تنظيف الأعمدة
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

def extend_realistic(x, target_len=3327):
    x = np.asarray(x, dtype=np.float64)

    if len(x) >= target_len:
        return x[:target_len]

    rng = np.random.default_rng(42)

    extended = list(x)

    while len(extended) < target_len:
        segment = x.copy()

        # 🔥 random scaling + jitter
        scale = rng.uniform(0.8, 1.2)
        noise = rng.normal(0, np.std(x)*0.05, len(segment))

        segment = scale * segment + noise

        extended.extend(segment)

    extended = np.array(extended[:target_len], dtype=np.float64)

    return extended
    
extended = extend_realistic(series, target_len=3327)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
