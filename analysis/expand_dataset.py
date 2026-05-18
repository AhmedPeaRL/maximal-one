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

df = pd.read_csv(INPUT_PATH, sep=";", engine="python")

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

def generate_structure(base, repeats=4):
    base = np.asarray(base, dtype=np.float64)

    base = base[np.isfinite(base)]
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for _ in range(repeats):
        n = len(base)

        start = rng.integers(0, int(0.3 * n))
        end = start + int(0.6 * n)

        segment = base[start:end].copy()

        # 🔥 NON-LINEAR DYNAMICS (بدل linear)
        for j in range(3, len(segment)):
            segment[j] = (
                0.6 * np.tanh(segment[j-1]) +
                0.25 * segment[j-2] * segment[j-3] +
                0.15 * np.sin(segment[j])
            )

        # 🔥 FRACTAL RESCALING
        scale = rng.uniform(0.8, 1.2)
        segment *= scale

        # 🔥 MULTI-SCALE MIX
        smooth1 = np.convolve(segment, np.ones(3)/3, mode="same")
        smooth2 = np.convolve(segment, np.ones(9)/9, mode="same")

        segment = 0.5 * segment + 0.3 * smooth1 + 0.2 * smooth2

        # 🔥 CONTROLLED NOISE (أضعف)
        segment += rng.normal(0, 0.01, len(segment))

        segments.append(segment)

    full = np.concatenate(segments)

    # 🔥 BREAK GLOBAL PERIODICITY
    full += 0.05 * np.random.standard_normal(len(full))

    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

# =========================
# RUN
# =========================
extended = generate_structure(series, repeats=6)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
