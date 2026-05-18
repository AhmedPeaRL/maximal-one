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

    n = len(base)
    out = np.zeros_like(base)

    # 🔥 persistent memory (long-range)
    H = 0.72  # Hurst-like control

    for i in range(1, n):
        # long memory kernel
        weights = np.exp(-np.arange(min(i, 50)) / (10 + 5 * H))
        weights /= np.sum(weights)

        memory = np.sum(out[i-len(weights):i] * weights[::-1])

        # innovation from base (scaled)
        innovation = 0.25 * base[i]

        # scale-adaptive noise
        noise_scale = 0.15 + 0.1 * (i / n)
        noise = rng.normal(0, noise_scale)

        out[i] = memory + innovation + noise

    # 🔥 global detrending
    trend = np.linspace(out[0], out[-1], n)
    out = out - trend * 0.3

    # 🔥 soft nonlinearity
    out = np.tanh(0.6 * out)

    # normalization
    out = (out - np.mean(out)) / (np.std(out) + 1e-12)

    return out
    
extended = generate_structure(series)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
