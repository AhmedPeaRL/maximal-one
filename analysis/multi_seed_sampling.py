import numpy as np
import json
import subprocess

SEEDS = [0,1,2,3,4,5,42,99,123]

alphas = []

for s in SEEDS:
    result = subprocess.check_output(
        ["python","scripts/generate_report.py","--seed",str(s),"--canonical"]
    )
    data = json.loads(open("artifacts/canonical_report.json").read())
    alphas.append(data["spectral_profile"]["estimated_alpha"])

mean_alpha = float(np.mean(alphas))
std_alpha  = float(np.std(alphas, ddof=1))

summary = {
    "mean_alpha": mean_alpha,
    "std_alpha": std_alpha
}

with open("artifacts/seed_statistics.json","w") as f:
    json.dump(summary,f,sort_keys=True)
