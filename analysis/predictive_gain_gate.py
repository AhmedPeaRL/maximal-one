import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg

rng = np.random.default_rng(42)

# --------------------------------
# Load dataset
# --------------------------------

data = pd.read_csv("data/predictions.csv")

# 🔥 FLEXIBLE COLUMN HANDLING
if "y_true" not in data.columns:
    raise SystemExit("predictions.csv must contain column: y_true")

if "hcm" in data.columns:
    hcm_col = "hcm"
elif "y_pred" in data.columns:
    hcm_col = "y_pred"
else:
    raise SystemExit("predictions.csv must contain either 'hcm' or 'y_pred'")

series = data["y_true"].to_numpy()

# --------------------------------
# Minimum dataset gate
# --------------------------------

MIN_POINTS = 20

if len(series) < MIN_POINTS:
    raise SystemExit(
        f"Dataset too small for predictive validation. "
        f"Found {len(series)} points, need at least {MIN_POINTS}."
    )

# --------------------------------
# Train / Test split
# --------------------------------

split = int(len(series) * 0.7)

train = series[:split]
test = series[split:]

if len(train) < 5:
    raise SystemExit("Training set too small for AR baseline.")

# --------------------------------
# Baseline model
# --------------------------------

ar_model = AutoReg(train, lags=1, old_names=False).fit()

baseline_pred = ar_model.predict(
    start=len(train),
    end=len(train) + len(test) - 1
)

# --------------------------------
# HCM predictions
# --------------------------------

hcm_pred = data[hcm_col].to_numpy()[split:]
y_true = test

# 🔥 ALIGN LENGTHS (CRITICAL FIX)
min_len = min(len(y_true), len(hcm_pred), len(baseline_pred))

y_true = y_true[:min_len]
hcm_pred = hcm_pred[:min_len]
baseline_pred = baseline_pred[:min_len]

# --------------------------------
# Bootstrap predictive gain
# --------------------------------

N_BOOT = 2000
gains = []

for _ in range(N_BOOT):

    idx = rng.choice(len(y_true), len(y_true), replace=True)

    mse_base = np.mean((y_true[idx] - baseline_pred[idx]) ** 2)
    mse_hcm = np.mean((y_true[idx] - hcm_pred[idx]) ** 2)

    gains.append(mse_base - mse_hcm)

gains = np.array(gains)

gain_mean = float(np.mean(gains))
p_value = float(np.mean(gains <= 0))

print("Predictive gain mean:", gain_mean)
print("p-value:", p_value)

if p_value < 0.05:
    print("Predictive superiority confirmed")
else:
    raise SystemExit("Predictive gain not statistically significant")
