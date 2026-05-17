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

        window_size = rng.integers(50, min(200, n))
        start = rng.integers(0, n - window_size)

        window = base[start:start + window_size].copy()

        for j in range(1, len(window)):
            window[j] = 0.85 * window[j-1] + 0.15 * window[j]

        window = np.tanh(window)

        noise = rng.normal(0, 0.2, len(window))
        window += noise

        segments.append(window)

    full = np.concatenate(segments)
    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

# =========================
# RUN
# =========================
extended = generate_structure(series, repeats=6)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
