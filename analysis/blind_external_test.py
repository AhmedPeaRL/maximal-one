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
    "structure_detected": alpha_est > 0.5
}

os.makedirs("artifacts", exist_ok=True)

with open(OUT, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
