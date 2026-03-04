import json
import numpy as np

with open("artifacts/lorenz.json") as f:
    d = json.load(f)

mse_naive = d["mse_naive"]
mse_hcm = d["mse_hcm"]

relative = (mse_naive - mse_hcm) / mse_naive

print("Relative improvement:", relative)

# Practical threshold: 1%
if relative < 0.01:
    raise SystemExit("Improvement not practically meaningful")
