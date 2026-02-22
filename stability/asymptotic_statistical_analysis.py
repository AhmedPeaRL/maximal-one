import json 
import numpy as np 
import sys from pathlib 
import Path from scipy 
import stats

REPORT_PATH = Path("core-scientific/analytic-number-theory/asymptotic_report.json")

if not REPORT_PATH.exists(): print("Asymptotic report not found.") sys.exit(1)

with open(REPORT_PATH) as f: data = json.load(f)

required_keys = [ "ratios", "n_values", "running_supremum", "max_ratio" ]

for key in required_keys: 
if key not in data: print(f"Missing key in report: {key}") sys.exit(1)

ratios = np.array(data["ratios"], dtype=float) n_values = np.array(data["n_values"], dtype=float) supremum = np.array(data["running_supremum"], dtype=float)

if len(ratios) < 200: print("Insufficient data for asymptotic analysis.") sys.exit(1)

----------------------------
Log-Log regression
----------------------------

log_n = np.log(n_values) 
log_ratio = np.log(ratios)

slope, intercept, r_value, p_value, std_err = stats.linregress(log_n, log_ratio)

decay_rate = -slope r_squared = r_value ** 2

----------------------------
Envelope decay verification
Compare early window vs late window
----------------------------

window = len(ratios) // 5

early_mean = np.mean(ratios[:window]) late_mean = np.mean(ratios[-window:])

envelope_decay = late_mean < early_mean

----------------------------
Supremum stabilization check
----------------------------

sup_change = np.max(np.abs(np.diff(supremum[-200:]))) sup_stable = sup_change < 1e-3

summary = { "sample_size": int(len(ratios)), "max_ratio": float(data["max_ratio"]), "estimated_decay_rate": float(decay_rate), "r_squared": float(r_squared), "p_value": float(p_value), "early_mean": float(early_mean), "late_mean": float(late_mean), "envelope_decay": bool(envelope_decay), "supremum_stable": bool(sup_stable) }

print(json.dumps(summary, indent=2))

----------------------------
Failure gates (revised)
----------------------------

if decay_rate <= 0: print("Non-decaying behaviour detected.") sys.exit(1)

if p_value > 1e-6: print("Decay not statistically significant.") sys.exit(1)

if not envelope_decay: print("Envelope not decreasing.") sys.exit(1)

if not sup_stable: print("Supremum not stabilized.") sys.exit(1)

if data["max_ratio"] > 1.0: print("Upper bound violation.") sys.exit(1)

print("Asymptotic statistical validation passed.")
