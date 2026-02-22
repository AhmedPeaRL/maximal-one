import json
import numpy as np
import sys
from pathlib import Path
from scipy import stats

REPORT_PATH = Path("core-scientific/analytic-number-theory/asymptotic_report.json")

if not REPORT_PATH.exists():
    print("Asymptotic report not found.")
    sys.exit(1)

with open(REPORT_PATH) as f:
    data = json.load(f)

if "ratios" not in data:
    print("Invalid asymptotic report structure.")
    sys.exit(1)

ratios = np.array(data["ratios"], dtype=float)
n_values = np.array(data["n_values"], dtype=float)

if len(ratios) < 10:
    print("Insufficient data for statistical analysis.")
    sys.exit(1)

# Linear regression on log-scale (to detect decay)
log_n = np.log(n_values)
log_ratio = np.log(ratios)

slope, intercept, r_value, p_value, std_err = stats.linregress(log_n, log_ratio)

decay_rate = -slope
confidence = r_value ** 2

summary = {
    "sample_size": int(len(ratios)),
    "mean_ratio": float(np.mean(ratios)),
    "max_ratio": float(np.max(ratios)),
    "min_ratio": float(np.min(ratios)),
    "estimated_decay_rate": float(decay_rate),
    "r_squared_confidence": float(confidence),
    "p_value": float(p_value)
}

print(json.dumps(summary, indent=2))

# CI failure conditions
if confidence < 0.85:
    print("Low regression confidence.")
    sys.exit(1)

if decay_rate < 0:
    print("Non-decaying or increasing behavior detected.")
    sys.exit(1)

print("Asymptotic statistical validation passed.")
