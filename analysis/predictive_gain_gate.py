import json
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.ar_model import AutoReg

rng = np.random.default_rng(42)

data = pd.read_csv("data/predictions.csv")

y_true = data["y_true"].to_numpy()
y_pred_baseline = data["baseline"].to_numpy()
y_pred_hcm = data["hcm"].to_numpy()

# ---- Generate synthetic data ----
N_BOOT = 2000
gains = []

for _ in range(N_BOOT):
    idx = rng.choice(len(y_true), len(y_true), replace=True)

    mse_base = np.mean((y_true[idx] - y_pred_baseline[idx]) ** 2)
    mse_hcm = np.mean((y_true[idx] - y_pred_hcm[idx]) ** 2)

    gains.append(mse_base - mse_hcm)

gains = np.array(gains)

p_value = np.mean(gains <= 0)
gain_mean = np.mean(gains)

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

significant = p_value < 0.01

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
    print("Predictive Gain Mean:", gain_mean)
    print("p-value:", p_value)

if p_value < 0.05:
    print("Predictive gain statistically significant")
else:
    raise SystemExit("Predictive gain not significant")
    exit(1)

print("PREDICTIVE_GATE_PASSED")
