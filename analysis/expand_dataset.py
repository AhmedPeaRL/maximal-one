import os
import pandas as pd
import numpy as np

# =========================
# CONFIG
# =========================
INPUT_PATH = "real-data/sunspots_full.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

# =========================
# LOAD (robust)
# =========================
if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

# auto-detect separator
df = pd.read_csv(INPUT_PATH, sep=None, engine="python")

# convert all to numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(axis=1, how="all")

# pick best numeric column
series = None
for col in df.columns:
    s = df[col].dropna().values
    if len(s) > 200 and np.std(s) > 1e-6:
        series = s
        break

if series is None:
    raise SystemExit("❌ No usable numeric column found")

series = series.astype(np.float64)

# =========================
# GENERATOR
# =========================
rng = np.random.default_rng(42)

def generate_structure(base, repeats=6):
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for _ in range(repeats):
        n = len(base)

        # 🔥 خليك تاخد segments طويلة
        window_size = rng.integers(int(0.4*n), int(0.8*n))
        start = rng.integers(0, n - window_size)

        window = base[start:start + window_size].copy()

        # 🔥 Long-range persistence (مش local smoothing)
        for j in range(2, len(window)):
            window[j] = (
                window[j]
                + 0.25 * np.sign(window[j-1]) * np.sqrt(abs(window[j-1]))
                - 0.15 * window[j-2]**2
            )

        # 🔥 بلاش tanh (بيقتل structure)
        # window = np.tanh(window)

        # 🔥 noise أخف بكتير
        noise = rng.normal(0, 0.05, len(window))
        window += noise

        segments.append(window)

    full = np.concatenate(segments)

    # 🔥 break permutation symmetry
    trend = np.linspace(-1, 1, len(full))
    full = full + 0.3 * trend * np.sign(full)

    coarse = full[::4]
    coarse = np.repeat(coarse, 4)[:len(full)]

    full = 0.7 * full + 0.3 * coarse
    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

# =========================
# RUN
# =========================
extended = generate_structure(series, repeats=6)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
