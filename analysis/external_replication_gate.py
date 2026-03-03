import json
import numpy as np

# ---- Load canonical report ----
with open("artifacts/canonical_report.json") as f:
    report = json.load(f)

if "synthetic_series" not in report:
    print("Missing synthetic_series in canonical_report.json")
    exit(1)

series = np.array(report["synthetic_series"])

# ---- Train/Test split ----
train = series[:400]
test = series[400:]

# ---- Baseline: closed-form linear regression ----
X = np.arange(len(train))
Y = train

# Least squares slope/intercept
A = np.vstack([X, np.ones(len(X))]).T
m, c = np.linalg.lstsq(A, Y, rcond=None)[0]

X_test = np.arange(len(train), len(series))
baseline_pred = m * X_test + c

baseline_mse = np.mean((test - baseline_pred)**2)

# ---- HCM metric ----
if "predictive_metrics" not in report:
    print("Missing predictive_metrics in canonical_report.json")
    exit(1)

hcm_mse = report["predictive_metrics"]["hcm_mse"]

delta = baseline_mse - hcm_mse

print("Baseline MSE:", baseline_mse)
print("HCM MSE:", hcm_mse)
print("Delta:", delta)

# ---- Strict Gate ----
if delta < 0:
    print("EXTERNAL_REPLICATION_FAILED")
    exit(1)

print("EXTERNAL_REPLICATION_PASSED")
