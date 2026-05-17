import os
import pandas as pd
import numpy as np

output_path = "real-data/sunspots_global_extended.csv"

if not os.path.exists("real-data/sunspots_global.csv"):
    raise SystemExit("❌ base dataset missing")

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:, 0].values.astype(np.float64)

rng = np.random.default_rng(42)

def generate_structure(base, repeats=6):

    base = np.asarray(base, dtype=np.float64)

    n = len(base)

    if n < 100:
        raise ValueError(f"Dataset too small: {n}")

    # normalize
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for i in range(repeats):

        # 🔥 adaptive window sizing
        max_window = min(300, n)
        min_window = min(150, n // 2)

        if max_window <= min_window:
            min_window = max(50, n // 3)

        window_size = rng.integers(min_window, max_window)

        # 🔥 safe start
        max_start = n - window_size

        if max_start <= 0:
            start = 0
        else:
            start = rng.integers(0, max_start)

        window = base[start:start + window_size].copy()

        # 🔥 controlled noise
        noise = rng.normal(0, 0.2, len(window))

        # 🔥 persistence
        for j in range(1, len(window)):
            window[j] = 0.85 * window[j-1] + 0.15 * window[j]

        # 🔥 nonlinear transform
        window = np.tanh(window * rng.uniform(0.8, 1.2))

        window = window + noise

        segments.append(window)

    full = np.concatenate(segments)

    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

extended = generate_structure(series, repeats=6)

# final normalization
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (ANTI-PERIODIC HARD):", len(extended))
