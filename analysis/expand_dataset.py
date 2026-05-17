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
# 🔥 TRUE SCALE-INVARIANT EXTENSION
# =========================

def generate_self_similar_series(base, repeats=6):

    base = np.asarray(base, dtype=np.float64)
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for i in range(repeats):

        # 🔥 random amplitude scaling (preserves structure)
        scale = 1.0 + np.random.uniform(-0.1, 0.1)

        # 🔥 slight shift
        shift = np.random.randint(0, len(base))
        shifted = np.roll(base, shift)

        # 🔥 very mild noise
        noise = np.random.normal(0, 0.01, len(base))

        new_segment = scale * shifted + noise

        segments.append(new_segment)

    return np.concatenate(segments)

extended = generate_self_similar_series(series, repeats=6)

# 🔥 final normalization
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (TRUE SCALE-INVARIANT):", len(extended))
