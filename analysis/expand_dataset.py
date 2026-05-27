import os
import pandas as pd
import numpy as np

INPUT_PATH = "real-data/sunspots_full.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

df = pd.read_csv(INPUT_PATH, sep=";", engine="python")
df = df.dropna(axis=1, how="all")

series = None
for col in df.columns:
    col_lower = col.lower()

    # 🚫 تجاهل الأعمدة الزمنية
    if any(k in col_lower for k in ["year", "date", "month"]):
        continue

    s = pd.to_numeric(df[col], errors="coerce").dropna().values

    if len(s) > 300 and np.std(s) > 1e-3:
        # 🔥 استبعد الأعمدة شبه الثابتة
        if np.unique(s[:50]).shape[0] < 10:
            continue

        series = s
        break

if series is None:
    raise SystemExit("❌ No usable numeric column found")

series = series.astype(np.float64)

def extend_realistic(x, target_len=3327):
    x = np.asarray(x, dtype=np.float64)

    if len(x) >= target_len:
        return x[:target_len]

    extended = list(x)
    rng = np.random.default_rng(42)

    while len(extended) < target_len:
        start = rng.integers(0, len(x) - 300)
        segment = x[start:start+300].copy()

        # 🔥 حافظ على structure
        scale = rng.uniform(0.8, 1.2)
        segment = segment * scale

        # 🔥 small noise فقط
        noise = rng.normal(0, np.std(segment)*0.05, len(segment))
        segment = segment + noise

        # 🔥 no differencing ❌❌❌

        extended.extend(segment.tolist())

    return np.array(extended[:target_len], dtype=np.float64)
    
extended = extend_realistic(series, target_len=3327)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
