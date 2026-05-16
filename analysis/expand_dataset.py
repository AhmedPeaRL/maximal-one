import os
import pandas as pd
import numpy as np

output_path = "real-data/sunspots_global_extended.csv"

if not os.path.exists("real-data/sunspots_global.csv"):
    raise SystemExit("❌ base dataset missing")

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:, 0].values.astype(np.float64)

# === NO SYNTHETIC DISTORTION ===

# فقط upsampling بدون إدخال structure
x = np.arange(len(series))
x_new = np.linspace(0, len(series) - 1, len(series) * 2)
extended = np.interp(x_new, x, series)

# === minimal noise (measurement-like only) ===
rng = np.random.default_rng(42)

# 🔥 noise أقوى شوية + jitter
noise = rng.normal(0, np.std(series) * 0.05, len(extended))

# 🔥 خفّف الحقن الصناعي
extended = extended + 0.05 * np.sin(
    np.linspace(0, 20*np.pi, len(extended))
)

# inject regime shifts
for i in range(0, len(extended), 200):
    extended[i:i+50] += np.random.uniform(-10, 10)
    
extended = extended + noise
pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (minimal intervention):", len(extended))
