import os
import pandas as pd
import numpy as np

INPUT_PATH = "real-data/sunspots_full.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

df = pd.read_csv(INPUT_PATH, sep=";", engine="python")

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

rng = np.random.default_rng(42)

def chaotic_transform(x):
    out = np.zeros_like(x)
    out[0] = x[0]

    for i in range(1, len(x)):
        out[i] = (
            0.6 * np.tanh(x[i-1]) +
            0.3 * np.sign(x[i-1]) * abs(x[i-1])**0.5 +
            0.1 * rng.normal()
        )

    return out

def generate_structure(base):
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    rng = np.random.default_rng(42)

    out = np.zeros_like(base)
    out[0] = base[0]

    for i in range(1, len(base)):

        # 🔥 تقليل الـ memory لتفادي resonance
        memory = 0.55 * out[i-1]

        # 🔥 إدخال decorrelation
        lag = rng.integers(1, 5)
        delayed = base[i-lag] if i-lag >= 0 else base[i]

        innovation = 0.3 * delayed

        # 🔥 noise أقوى شوية
        noise = rng.normal(0, 0.25)

        out[i] = memory + innovation + noise

    # 🔥 إزالة أي trend دوري خفي
    out = out - np.convolve(out, np.ones(15)/15, mode='same')

    # 🔥 non-linearity خفيفة
    out = np.tanh(0.8 * out)

    # normalization
    out = (out - np.mean(out)) / (np.std(out) + 1e-12)

    return out
    
extended = generate_structure(series)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
