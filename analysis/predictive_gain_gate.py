import numpy as np
import json
from scipy import stats
from statsmodels.tsa.ar_model import AutoReg

np.random.seed(42)

# ---- synthetic dataset ----
N = 500
noise = np.random.normal(0, 0.1, N)
series = np.zeros(N)
phi = 0.8

for t in range(1, N):
    series[t] = phi * series[t-1] + noise[t]

# ---- split ----
train_size = 400
train = series[:train_size]
test = series[train_size:]

# ---- AR(1) baseline ----
ar_model = AutoReg(train, lags=1, old_names=False).fit()
ar_pred = ar_model.predict(start=train_size, end=N-1)
ar_errors = (test - ar_pred) ** 2

# ---- HCM kernel ----
alpha = 0.5
hcm_pred = []
last = train[-1]

for t in range(len(test)):
    pred = (1 - alpha) * last + alpha * np.tanh(last)
    hcm_pred.append(pred)
    last = test[t]

hcm_pred = np.array(hcm_pred)
hcm_errors = (test - hcm_pred) ** 2

# ---- statistics ----
delta = np.mean(ar_errors) - np.mean(hcm_errors)
relative = delta / np.mean(ar_errors)

t_stat, p_value = stats.ttest_rel(ar_errors, hcm_errors)

result = {
    "ar_mse": float(np.mean(ar_errors)),
    "hcm_mse": float(np.mean(hcm_errors)),
    "delta_mse": float(delta),
    "relative_gain": float(relative),
    "t_stat": float(t_stat),
    "p_value": float(p_value),
    "significant": bool(p_value < 0.05),
}

print(json.dumps(result, indent=2))

# ---- scientific gate ----
tolerance = 0.0

if delta < -tolerance and p_value < 0.05:
    print("HCM_SIGNIFICANTLY_WORSE")
    exit(1)
else:
    print("PREDICTIVE_GATE_PASSED")
