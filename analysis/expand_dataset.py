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
block_size = 32

for _ in range(len(series) // block_size):
    start = rng.integers(0, len(series) - block_size)
    blocks.extend(series[start:start + block_size])

extended = np.array(blocks, dtype=np.float64)

# 🔥 preserve structure instead of destroying it
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (BLOCK-RESAMPLED):", len(extended))
