import json
import glob
import numpy as np
import math
from collections import defaultdict

THRESHOLD_CV = 0.3  # key threshold

features = defaultdict(list)

TARGET_KEYS = [
    "entropy_rate",
    "spectral_alpha",
    "hurst_exponent",
    "attractor_dimension",
    "lyapunov_exp",
    "alpha",
    "estimated_alpha"
]

def extract(obj):

    if isinstance(obj, dict):
        for k,v in obj.items():

            if k in TARGET_KEYS and isinstance(v,(int,float)):
                if not math.isnan(v) and not math.isinf(v):
                    features[k].append(float(v))

            extract(v)

    elif isinstance(obj,list):
        for v in obj:
            extract(v)


for f in glob.glob("artifacts/*.json"):
    try:
        with open(f) as fh:
            data=json.load(fh)
        extract(data)
    except:
        pass


results = []

for k,vals in features.items():

    if len(vals) < 5:
        continue

    vals = np.array(vals)

    mean = float(np.mean(vals))
    std = float(np.std(vals))

    cv = std / (abs(mean) + 1e-9)

    results.append({
        "feature": k,
        "samples": len(vals),
        "mean": mean,
        "std": std,
        "cv": cv,
        "stable": cv < THRESHOLD_CV
    })


# sort by stability
results.sort(key=lambda x: x["cv"])

passed = any(r["stable"] for r in results)

output = {
    "features": results,
    "stable_features": [r for r in results if r["stable"]],
    "passed": passed
}

print(json.dumps(output, indent=2))
