import json
import numpy as np
from .numerical_spectral_verification import estimate_alpha

# Recompute spectral amplitudes deterministically
np.random.seed(42)

series = np.random.normal(0,1,1024)

# Compute baseline alpha
baseline_alpha = estimate_alpha(series)

# Bootstrap
boot = []
for _ in range(200):
    idx = np.random.choice(len(series), len(series), replace=True)
    sample = series[idx]
    boot.append(estimate_alpha(sample))

boot = np.array(boot)

result = {
    "baseline_alpha": float(baseline_alpha),
    "bootstrap_mean": float(np.mean(boot)),
    "bootstrap_std": float(np.std(boot)),
}

print(json.dumps(result, indent=2))
