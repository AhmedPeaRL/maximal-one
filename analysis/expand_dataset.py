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

        # 🔥 random slice
        start = rng.integers(0, len(base) // 2)
        length = rng.integers(len(base)//4, len(base))
        window = base[start:start+length]

        # 🔥 NON-UNIFORM RESAMPLING (CRITICAL FIX)
        target_len = rng.integers(len(base)//2, int(len(base)*1.5))

        x_old = np.linspace(0, 1, len(window))
        x_new = np.sort(rng.uniform(0, 1, target_len))  # 🔥 irregular grid

        warped = np.interp(x_new, x_old, window)

        # 🔥 random cut again (kills structure memory)
        cut_start = rng.integers(0, len(warped)//3)
        cut_len = rng.integers(len(warped)//2, len(warped))
        warped = warped[cut_start:cut_start+cut_len]

        # 🔥 nonlinear distortion (stronger)
        distorted = np.sign(warped) * (np.abs(warped) ** rng.uniform(0.6, 0.9))

        # 🔥 amplitude randomization
        scale = rng.uniform(0.5, 1.5)

        # 🔥 adaptive noise (important)
        noise = rng.normal(0, 0.03 * np.std(distorted), len(distorted))

        segment = scale * distorted + noise

        segments.append(segment)

    # 🔥 concatenate WITHOUT forcing equal lengths
    full = np.concatenate(segments)

    # 🔥 FINAL RANDOM RESAMPLING (DESTROYS GLOBAL PERIODICITY)
    target_final = len(base) * repeats

    x_old = np.linspace(0, 1, len(full))
    x_new = np.sort(rng.uniform(0, 1, target_final))

    final = np.interp(x_new, x_old, full)

    return final

extended = generate_structure(series, repeats=6)

# final normalization
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (ANTI-PERIODIC HARD):", len(extended))
