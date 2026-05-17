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

    # normalize
    base = (base - np.mean(base)) / (np.std(base) + 1e-12)

    segments = []

    for i in range(repeats):

        # 🔥 take contiguous chunk (preserve structure)
        start = rng.integers(0, len(base) - 200)
        window = base[start:start + rng.integers(150, 300)]

        # 🔥 controlled noise (NOT destructive)
        noise = rng.normal(0, 0.2, len(window))

        # 🔥 persistent mixing (keeps memory)
        for j in range(1, len(window)):
            window[j] = 0.85 * window[j-1] + 0.15 * window[j]

        # 🔥 mild nonlinear transform (NOT killing spectrum)
        window = np.tanh(window * rng.uniform(0.8, 1.2))

        # 🔥 add noise
        window = window + noise

        segments.append(window)

    full = np.concatenate(segments)

    # 🔥 FINAL LIGHT NORMALIZATION (NO DESTRUCTION)
    full = (full - np.mean(full)) / (np.std(full) + 1e-12)

    return full

extended = generate_structure(series, repeats=6)

# final normalization
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (ANTI-PERIODIC HARD):", len(extended))
