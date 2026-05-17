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
# 🔥 TRUE NON-PERIODIC SCALE STRUCTURE
# =========================

def generate_structure(base, repeats=6):

    base = np.asarray(base, dtype=np.float64)
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for i in range(repeats):

        # 🔥 random window instead of full copy
        start = rng.integers(0, len(base) // 2)
        length = rng.integers(len(base)//4, len(base))

        window = base[start:start+length]

        # 🔥 random resampling (kills periodic alignment)
        indices = np.linspace(
            0,
            len(window) - 1,
            len(base)
        )

        warped = np.interp(
            indices,
            np.arange(len(window)),
            window
        )

        # 🔥 amplitude variation
        scale = rng.uniform(0.7, 1.3)

        # 🔥 controlled nonlinear transformation (preserves structure)
        distorted = np.sign(warped) * (np.abs(warped) ** 0.75)

        # 🔥 LOW noise (critical fix)
        noise = rng.normal(0, 0.015, len(base))

        segment = scale * distorted + noise

        segments.append(segment)

    full = np.concatenate(segments)

    return full

extended = generate_structure(series, repeats=6)

# final normalization
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (ANTI-PERIODIC):", len(extended))
