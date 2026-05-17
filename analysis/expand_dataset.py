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
# 🔥 TRUE NON-PERIODIC STRUCTURE (FIXED)
# =========================

def generate_structure(base, repeats=6):

    base = np.asarray(base, dtype=np.float64)
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for i in range(repeats):

        # 🔥 completely random subspace projection
        idx = rng.choice(len(base), size=rng.integers(50, len(base)), replace=False)
        window = base[idx]

        # 🔥 random permutation (DESTROYS ORDER MEMORY)
        window = rng.permutation(window)

        # 🔥 random nonlinear mixing
        mix = rng.normal(0, 1, len(window))
        window = 0.7 * window + 0.3 * mix

        # 🔥 chaotic warping (NOT interpolation-based)
        warped = np.tanh(window * rng.uniform(0.5, 2.5))

        # 🔥 stochastic differential evolution step
        for _ in range(3):
            noise = rng.normal(0, 0.1, len(warped))
            warped = warped + noise * np.gradient(warped)

        # 🔥 break any residual structure
        warped = rng.permutation(warped)

        segments.append(warped)

    full = np.concatenate(segments)

    # 🔥 FINAL DESTRUCTIVE MIX
    noise = rng.normal(0, np.std(full)*0.5, len(full))
    full = 0.6 * full + 0.4 * noise

    # 🔥 normalize
    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

extended = generate_structure(series, repeats=6)

# final normalization
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (ANTI-PERIODIC HARD):", len(extended))
