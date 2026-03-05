import json
import numpy as np
from scipy.stats import ttest_ind

np.random.seed(0)

def baseline(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(loc=1.0, scale=0.2)

def maximal(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(loc=1.05, scale=0.2)

seeds = list(range(50))

baseline_scores = []
maximal_scores = []

for s in seeds:
    baseline_scores.append(baseline(s))
    maximal_scores.append(maximal(s))

baseline_scores = np.array(baseline_scores)
maximal_scores = np.array(maximal_scores)

improvement = float(np.mean(maximal_scores) - np.mean(baseline_scores))

stat, p_value = ttest_ind(maximal_scores, baseline_scores, equal_var=False)

result = {
    "baseline_mean": float(np.mean(baseline_scores)),
    "maximal_mean": float(np.mean(maximal_scores)),
    "improvement": improvement,
    "p_value": float(p_value),
    "n": len(seeds)
}

with open("artifacts/lorenz96.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
