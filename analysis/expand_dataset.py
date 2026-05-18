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

# 🔥 FIXED CHAOTIC TRANSFORM (NO PERIODICITY)
def chaotic_transform(x):
    out = np.zeros_like(x)
    out[:3] = x[:3]

    for i in range(3, len(x)):
        out[i] = (
            0.45 * np.tanh(x[i-1]) +
            0.25 * x[i-2] * np.sign(x[i-3]) +
            0.2 * np.log1p(abs(x[i])) * np.sign(x[i]) +
            0.1 * rng.normal()
        )

    return out

def generate_structure(base):
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for _ in range(8):
        n = len(base)

        start = rng.integers(0, int(0.6 * n))
        length = rng.integers(int(0.3 * n), int(0.6 * n))

        segment = base[start:start+length]

        if len(segment) < 100:
            continue

        segment = chaotic_transform(segment)

        # 🔥 REDUCED MEMORY (CRITICAL FIX)
        for i in range(1, len(segment)):
            segment[i] += 0.45 * segment[i-1]

        # 🔥 RANDOM RESAMPLING بدل warp
        idx = np.sort(rng.choice(len(segment), size=len(segment), replace=True))
        segment = segment[idx]

        # 🔥 NOISE CONTROLLED
        noise = rng.normal(0, 0.3 * np.std(segment), len(segment))
        segment = segment + noise

        segments.append(segment)

    full = np.concatenate(segments)

    # 🔥 STRUCTURE-PRESERVING MIX (بديل آمن)
    mix_strength = 0.15
    shift = rng.integers(1, len(full)//10)

    full = (
        (1 - mix_strength) * full +
        mix_strength * np.roll(full, shift)
    )

    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

extended = generate_structure(series)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
