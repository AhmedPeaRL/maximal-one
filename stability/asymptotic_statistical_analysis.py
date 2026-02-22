import json
import numpy as np
import sys
from pathlib import Path
from scipy import stats

"""
Asymptotic Statistical Analysis
--------------------------------
This module performs numerical asymptotic verification
for the ratio tau(n) / (2 * sqrt(n)) up to finite N.

IMPORTANT:
This is numerical evidence, not a formal proof
for all natural numbers.
"""

REPORT_PATH = Path("core-scientific/analytic-number-theory/asymptotic_report.json")

if not REPORT_PATH.exists():
    print("Asymptotic report not found.")
    sys.exit(1)

with open(REPORT_PATH, "r") as f:
    data = json.load(f)

required_keys = [
    "ratios",
    "n_values",
    "running_supremum",
    "max_ratio"
]

for key in required_keys:
    if key not in data:
        print(f"Missing key in report: {key}")
        sys.exit(1)

ratios = np.array(data["ratios"], dtype=float)
n_values = np.array(data["n_values"], dtype=float)
supremum = np.array(data["running_supremum"], dtype=float)

if len(ratios) < 200:
    print("Insufficient data for asymptotic analysis.")
    sys.exit(1)

# ---------------------------------------
# Log-Log regression
# ---------------------------------------

log_n = np.log(n_values)
log_ratio = np.log(ratios)

slope, intercept, r_value, p_value, std_err = stats.linregress(log_n, log_ratio)

decay_rate = -slope
r_squared = r_value ** 2

# ---------------------------------------
# Spearman monotonicity test
# ---------------------------------------

spearman_corr, spearman_p = stats.spearmanr(n_values, ratios)

# ---------------------------------------
# Envelope decay verification
# ---------------------------------------

window = len(ratios) // 5

early_mean = np.mean(ratios[:window])
late_mean = np.mean(ratios[-window:])

envelope_decay = late_mean < early_mean

# ---------------------------------------
# Rolling window monotonic smoothing
# ---------------------------------------

rolling_window = 200
rolling_means = np.convolve(
    ratios,
    np.ones(rolling_window) / rolling_window,
    mode="valid"
)

rolling_decay = rolling_means[-1] < rolling_means[0]

# ---------------------------------------
# Supremum stabilization
# ---------------------------------------

if len(supremum) > 200:
    sup_segment = supremum[-200:]
else:
    sup_segment = supremum

sup_change = np.max(np.abs(np.diff(sup_segment)))
sup_stable = sup_change < 1e-3

# ---------------------------------------
# Summary
# ---------------------------------------

summary = {
    "sample_size": int(len(ratios)),
    "max_ratio": float(data["max_ratio"]),
    "estimated_decay_rate": float(decay_rate),
    "r_squared": float(r_squared),
    "p_value_loglog": float(p_value),
    "spearman_correlation": float(spearman_corr),
    "spearman_p_value": float(spearman_p),
    "early_mean": float(early_mean),
    "late_mean": float(late_mean),
    "envelope_decay": bool(envelope_decay),
    "rolling_decay": bool(rolling_decay),
    "supremum_stable": bool(sup_stable)
}

print(json.dumps(summary, indent=2))

# ---------------------------------------
# Failure Gates
# ---------------------------------------

if decay_rate <= 0:
    print("Non-decaying behaviour detected.")
    sys.exit(1)

if p_value > 1e-6:
    print("Log-log decay not statistically significant.")
    sys.exit(1)

if spearman_corr >= 0:
    print("Spearman monotonicity violation.")
    sys.exit(1)

if not envelope_decay:
    print("Envelope not decreasing.")
    sys.exit(1)

if not rolling_decay:
    print("Rolling average not decreasing.")
    sys.exit(1)

if not sup_stable:
    print("Supremum not stabilized.")
    sys.exit(1)

if data["max_ratio"] > 1.0:
    print("Upper bound violation.")
    sys.exit(1)

print("Asymptotic statistical validation passed.")
