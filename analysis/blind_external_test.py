import pandas as pd
import numpy as np
import json
import os

OUT = "artifacts/blind_test.json"

# simulate unseen dataset
np.random.seed(42)
data = np.cumsum(np.random.normal(size=1000))

# compute simple spectral proxy
alpha_est = np.mean(np.abs(np.diff(data)))

result = {
    "alpha_proxy": float(alpha_est),
    "structure_detected": bool(alpha_est > 0.5)
}

os.makedirs("artifacts", exist_ok=True)

def safe_json(obj):
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    return str(obj)

with open(OUT, "w") as f:
    json.dump(result, f, indent=2, default=safe_json)

print(json.dumps(result, indent=2))
