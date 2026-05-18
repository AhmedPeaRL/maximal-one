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

    segments = []

    for _ in range(6):  # reduced complexity
        start = rng.integers(0, len(base)//2)
        length = rng.integers(len(base)//4, len(base)//2)

        segment = base[start:start+length]

        if len(segment) < 100:
            continue

        segment = chaotic_transform(segment)

        # remove feedback amplification (IMPORTANT FIX)
        segment = np.convolve(segment, np.ones(3)/3, mode="same")

        noise = rng.normal(0, 0.2, len(segment))
        segment = segment + noise

        segments.append(segment)

    full = np.concatenate(segments)

    # NO SHIFT MIXING
    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

extended = generate_structure(series)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
