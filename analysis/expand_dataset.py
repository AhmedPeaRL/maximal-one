import os
import pandas as pd
import numpy as np

output_path = "real-data/sunspots_global_extended.csv"

if not os.path.exists("real-data/sunspots_global.csv"):
    raise SystemExit("❌ base dataset missing")

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:, 0].values.astype(np.float64)

x = np.arange(len(series))
x_new = np.linspace(0, len(series) - 1, len(series) * 2)

# interpolation base
extended = np.interp(x_new, x, series)

rng = np.random.default_rng(42)

# 🔥 step 1: local variance modulation (break stationarity)
window = 12
local_std = np.array([
    np.std(extended[max(0, i-window):i+1]) + 1e-6
    for i in range(len(extended))
])

modulation = rng.normal(0, local_std * 0.15)

# 🔥 step 2: nonlinear distortion (break phase symmetry)
nonlinear = 0.03 * (extended ** 1.5) / (np.max(np.abs(extended)) + 1e-6)

# 🔥 step 3: structured perturbation (NOT white noise)
structured = np.sin(np.linspace(0, 8*np.pi, len(extended))) * np.std(series) * 0.05

extended = extended + modulation + nonlinear + structured

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (nonlinear + nonstationary):", len(extended))
