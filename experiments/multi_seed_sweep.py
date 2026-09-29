import numpy as np
import os
import json
import pandas as pd
from scipy import stats

"""
SCIENTIFIC ROLE: SYNTHETIC / METHODOLOGICAL ONLY.

This experiment does not provide empirical evidence
for the HCM spectral-persistence hypothesis.

Its outputs MUST NOT be used as:
- effect-size evidence for real data,
- independent replication,
- statistical significance for the primary claim,
- evidence of prediction,
- evidence of causality,
- evidence of HCM validity.

Any zero-variance or degenerate comparison is invalid.
"""

def run_baseline(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0.5, 0.05)

def run_model(seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0.48, 0.05)

os.makedirs("../data", exist_ok=True)
os.makedirs("artifacts", exist_ok=True)

seeds = range(200)

baseline = []
model = []

for s in seeds:
    baseline.append(run_baseline(s))
    model.append(run_model(s))

baseline = np.array(baseline)
model = np.array(model)

score_difference = baseline - model

df = pd.DataFrame({
    "baseline": baseline,
    "model": model,
    "score_difference": score_difference
})

output_path = "../data/multi_seed_results.csv"

df.to_csv(output_path, index=False)

# 🔒 ضمان إن الملف مش فاضي
if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
    raise RuntimeError("Dataset write failed: empty file")

# stats
improvement = baseline.mean() - model.mean()
t, p = stats.ttest_ind(baseline, model)

result = {
    "baseline_mean": float(baseline.mean()),
    "model_mean": float(model.mean()),
    "improvement": float(improvement),
    "p_value": float(p),
    "n_seeds": len(seeds),
    "system": "synthetic_score_sweep",
    "scientific_role": "diagnostic_only",
    "independent_real_domain_evidence": False,
    "lorenz96_validation": False,
    "claim_support_eligible": False,
    "status": "generated"
}

with open("artifacts/synthetic_seed_sweep.json", "w") as f:
    json.dump(result, f, indent=2)

print(result)
