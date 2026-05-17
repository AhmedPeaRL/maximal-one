import os
import pandas as pd
import numpy as np

# =========================
# CONFIG
# =========================
INPUT_PATH = "real-data/sunspots_full.csv, real-data/airline_passengers.csv, real-data/temperature_global.csv, real-data/co2.csv, real-data/earthquake_magnitude_clean.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

# =========================
# VALIDATION
# =========================
if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

# =========================
# LOAD
# =========================
df = pd.read_csv(INPUT_PATH, sep=';')

# اختيار العمود الحقيقي (القيم الشمسية)
series = df.iloc[:, 3].values.astype(np.float64)

# تنظيف
series = series[np.isfinite(series)]

if len(series) < 200:
    raise SystemExit("❌ Dataset too small after cleaning")

# =========================
# GENERATOR
# =========================
rng = np.random.default_rng(42)

def generate_structure(base, repeats=6):

    base = np.asarray(base, dtype=np.float64)
    n = len(base)

    # normalize
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for _ in range(repeats):

        max_window = min(300, n)
        min_window = min(150, n // 2)

        if max_window <= min_window:
            min_window = max(50, n // 3)

        window_size = rng.integers(min_window, max_window)

        max_start = n - window_size
        start = 0 if max_start <= 0 else rng.integers(0, max_start)

        window = base[start:start + window_size].copy()

        # persistence
        for j in range(1, len(window)):
            window[j] = 0.85 * window[j-1] + 0.15 * window[j]

        # nonlinear transform
        window = np.tanh(window * rng.uniform(0.8, 1.2))

        # noise
        noise = rng.normal(0, 0.2, len(window))
        window = window + noise

        segments.append(window)

    full = np.concatenate(segments)

    # final normalization
    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

# =========================
# RUN
# =========================
extended = generate_structure(series, repeats=6)

pd.DataFrame({"Sunspots": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
