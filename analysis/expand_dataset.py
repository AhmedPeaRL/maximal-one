import os
import pandas as pd
import numpy as np

output_path = "real-data/sunspots_global_extended.csv"

if not os.path.exists("real-data/sunspots_global.csv"):
    raise SystemExit("❌ base dataset missing")

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:, 0].values.astype(np.float64)

# ✅ بدل duplication → interpolation ناعم
x = np.arange(len(series))
x_new = np.linspace(0, len(series) - 1, len(series) * 2)

extended = np.interp(x_new, x, series)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (interpolated):", len(extended))
