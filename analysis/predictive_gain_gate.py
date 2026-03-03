import numpy as np
import json
from scipy import stats

# assume ar_errors and hcm_errors are rolling error arrays

delta = np.mean(ar_errors) - np.mean(hcm_errors)
relative = delta / np.mean(ar_errors)

t_stat, p_value = stats.ttest_rel(ar_errors, hcm_errors)

result = {
    "delta_mse": float(delta),
    "relative_gain": float(relative),
    "t_stat": float(t_stat),
    "p_value": float(p_value),
    "significant": bool(p_value < 0.05),
    "passed": bool(delta > 0 or p_value > 0.05)
}

print(json.dumps(result))
