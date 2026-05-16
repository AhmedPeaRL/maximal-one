import os
import pandas as pd
import numpy as np

output_path = "real-data/sunspots_global_extended.csv"

if not os.path.exists("real-data/sunspots_global.csv"):
    raise SystemExit("❌ base dataset missing")

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:, 0].values.astype(np.float64)

# 🔥 بدل interpolation → block-resampling (يحافظ على structure)
rng = np.random.default_rng(42)

blocks = []
block_size = 8

for _ in range(len(series) // block_size):
    start = rng.integers(0, len(series) - block_size)
    blocks.extend(series[start:start + block_size])

extended = np.array(blocks, dtype=np.float64)

# 🔥 minimal noise (مش smoothing)
noise = rng.normal(0, np.std(series) * 0.02, len(extended))
extended = extended + noise
extended = np.diff(extended, prepend=extended[0])

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (BLOCK-RESAMPLED):", len(extended))
