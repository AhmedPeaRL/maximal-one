import os
import pandas as pd
import numpy as np

# =========================
# CONFIG
# =========================
INPUT_PATH = "real-data/airline_passengers.csv"
INPUT_PATH = "real-data/sunspots_full.csv"
INPUT_PATH = "real-data/temperature_global.csv"
INPUT_PATH = "real-data/co2.csv"
INPUT_PATH = "real-data/co2_atmospheric.csv"
INPUT_PATH = "real-data/cosmic_rays.csv"
INPUT_PATH = "real-data/earthquake_magnitude.csv"
INPUT_PATH = "real-data/solar_wind_speed.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

# =========================
# VALIDATION
# =========================
if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

# =========================
# LOAD
# =========================
df = pd.read_csv(INPUT_PATH)
series = df.iloc[:, 3]

series = pd.to_numeric(series, errors="coerce")
series = series.dropna().values.astype(np.float64)
series = series[np.isfinite(series)]

if "Passengers" not in df.columns:
    raise SystemExit("❌ Column 'Passengers' not found")

series = df["Passengers"].dropna().values.astype(np.float64)

if len(series) < 100:
    raise SystemExit("❌ Dataset too small")

# =========================
# GENERATOR
# =========================
rng = np.random.default_rng(42)

def generate_structure(base, repeats=6):
    base = np.asarray(base, dtype=np.float64)

    # normalize
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for _ in range(repeats):
        n = len(base)

        window_size = rng.integers(50, min(200, n))
        start = rng.integers(0, n - window_size)

        window = base[start:start + window_size].copy()

        # persistence
        for j in range(1, len(window)):
            window[j] = 0.85 * window[j-1] + 0.15 * window[j]

        # nonlinear transform
        window = np.tanh(window)

        # noise
        noise = rng.normal(0, 0.2, len(window))
        window += noise

        segments.append(window)

    full = np.concatenate(segments)

    # normalize again
    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

# =========================
# RUN
# =========================
extended = generate_structure(series, repeats=6)

pd.DataFrame({"Sunspots": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
