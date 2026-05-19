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

# ✅ EXTENSION بدون قتل الطاقة
def extend_realistic(x, target_len=3327):
    x = np.asarray(x, dtype=np.float64)

    n = len(x)
    out = list(x)

    rng = np.random.default_rng(42)

    while len(out) < target_len:
        idx = rng.integers(0, n - 120)
        chunk = x[idx:idx+120]

        # 🔥 حافظ على amplitude
        scale = 1.0 + rng.normal(0, 0.01)

        # 🔥 noise ضعيف جداً
        noise = rng.normal(0, np.std(x)*0.005, len(chunk))

        new_chunk = scale * chunk + noise
        out.extend(new_chunk)

    out = np.array(out[:target_len])
    
    return out

extended = extend_realistic(series, target_len=3327)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
