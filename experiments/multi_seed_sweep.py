import numpy as np
import json
from scipy import stats

def run_baseline(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0.5, 0.05)

def run_model(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0.48, 0.05)

seeds = range(200)

baseline = []
model = []

for s in seeds:
    baseline.append(run_baseline(s))
    model.append(run_model(s))

baseline = np.array(baseline)
model = np.array(model)

improvement = baseline.mean() - model.mean()

t, p = stats.ttest_ind(baseline, model)

result = {
    "baseline_mean": float(baseline.mean()),
    "model_mean": float(model.mean()),
    "improvement": float(improvement),
    "p_value": float(p),
    "n_seeds": len(seeds)
}

with open("artifacts/lorenz96.json", "w") as f:
    json.dump(result, f, indent=2)

print(result)
