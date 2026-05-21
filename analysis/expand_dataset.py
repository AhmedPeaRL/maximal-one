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

    # ✅ bootstrap blocks بدل AR
    rng = np.random.default_rng(42)
    block_size = rng.integers(32, 96)

    out = []

    while len(out) < target_len:
        block_size = rng.integers(32, 96)
        start = rng.integers(0, len(x) - block_size)
        block = x[start:start+block_size]

        # 🔥 jitter بسيط يمنع periodicity
        noise = rng.normal(0, 0.01 * np.std(x), size=len(block))
        block = block + noise

        out.extend(block)

    return np.array(out[:target_len])

extended = extend_realistic(series, target_len=3327)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
