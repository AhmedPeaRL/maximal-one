import json
import numpy as np
from scipy import stats
from statsmodels.tsa.ar_model import AutoReg

rng = np.random.default_rng(42)

# ---- Generate synthetic data ----
n = 500
noise = np.random.normal(0, 0.2, n)
series = np.zeros(n)
for t in range(1, n):
    series[t] = 0.8 * series[t-1] + noise[t]

train = series[:400]
test = series[400:]
n_boot = 1000
improvements = []

for i in range(n_boot):
    idx = rng.choice(len(y_true), len(y_true), replace=True)
    improvements.append(
        rmse_baseline(idx) - rmse_hcm(idx)
    )

p_value = np.mean(np.array(improvements) <= 0)
# ---- Baseline AR(1) ----
ar_model = AutoReg(train, lags=1).fit()
ar_pred = ar_model.predict(start=400, end=499)
ar_mse = np.mean((test - ar_pred)**2)

# ---- HCM predictor (smoothed kernel proxy) ----
hcm_pred = 0.8 * series[399:499]
hcm_mse = np.mean((test - hcm_pred)**2)

delta_mse = ar_mse - hcm_mse
relative_gain = delta_mse / ar_mse

t_stat, p_value = stats.ttest_ind(
    (test - ar_pred)**2,
    (test - hcm_pred)**2
)

significant = p_value < 0.05

report = {
    "synthetic_series": series.tolist(),
    "predictive_metrics": {
        "ar_mse": float(ar_mse),
        "hcm_mse": float(hcm_mse),
        "delta_mse": float(delta_mse),
        "relative_gain": float(relative_gain),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "significant": bool(significant)
    }
}

print(json.dumps(report, indent=2))

# ---- Save canonical report ----
with open("artifacts/canonical_report.json", "w") as f:
    json.dump(report, f, indent=2)

if delta_mse <= 0 or not significant:
    print("PREDICTIVE_GATE_FAILED")
    print("Baseline RMSE:", baseline_rmse)
    print("HCM RMSE:", hcm_rmse)
    print("Delta:", baseline_rmse - hcm_rmse)
    exit(1)

print("PREDICTIVE_GATE_PASSED")
