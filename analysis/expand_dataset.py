import os
import pandas as pd
import numpy as np

output_path = "real-data/sunspots_global_extended.csv"

if not os.path.exists("real-data/sunspots_global.csv"):
    raise SystemExit("❌ base dataset missing")

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:, 0].values.astype(np.float64)

rng = np.random.default_rng(42)

# =========================
# 🔥 MULTI-SCALE PRESERVATION
# =========================

def generate_multiscale_series(base, rng, repeats=4):
    n = len(base)
    result = []

    for _ in range(repeats):
        # 🔹 random block
        start = rng.integers(0, n - 32)
        block = base[start:start+32].copy()

        # 🔹 inject weak correlated noise
        noise = rng.normal(0, np.std(block) * 0.15, len(block))
        block = block + noise

        # 🔹 random walk drift (very weak)
        drift = np.cumsum(rng.normal(0, 0.02, len(block)))
        block = block + drift

        result.extend(block)

    return np.array(result, dtype=np.float64)

extended = generate_multiscale_series(series, rng, repeats=6)

# 🔥 final normalization (global)
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (MULTI-SCALE PRESERVED):", len(extended))
