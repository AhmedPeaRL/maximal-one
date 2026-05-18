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
    out[0:3] = x[0:3]

    for i in range(3, len(x)):
        out[i] = (
            0.4 * np.tanh(x[i-1]) +
            0.3 * x[i-2] * np.cos(x[i-3]) +
            0.2 * np.sin(x[i]) +
            0.1 * rng.normal()
        )

    return out

def generate_structure(base):
    base = base.copy()
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for _ in range(8):
        n = len(base)

        start = rng.integers(0, int(0.5 * n))
        length = rng.integers(int(0.3 * n), int(0.7 * n))

        segment = base[start:start+length]

        if len(segment) < 100:
            continue

        segment = chaotic_transform(segment)

        # 🔥 reinforce temporal memory
        for i in range(1, len(segment)):
            segment[i] += 0.6 * segment[i-1]

        warp = np.linspace(0, 1, len(segment))
        warp = warp ** rng.uniform(0.8, 1.2)
        segment = np.interp(warp, np.linspace(0,1,len(segment)), segment)

        noise = rng.normal(0, np.std(segment), len(segment))
        segment = 0.9 * segment + 0.1 * noise

        segments.append(segment)

    full = np.concatenate(segments)

    full += rng.normal(0, 0.05, len(full))

    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

extended = generate_structure(series)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
