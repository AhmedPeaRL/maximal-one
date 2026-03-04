import json
import sys

with open("artifacts/lorenz.json") as f:
    d = json.load(f)

mse_naive = d["mse_naive"]
mse_hcm = d["mse_hcm"]

relative = (mse_naive - mse_hcm) / mse_naive

print("Relative improvement:", relative)

threshold = 0.01  # 1% practical threshold

if relative < threshold:
    print("WARNING: Improvement below practical threshold.")
    sys.exit(0)   # report only, do not fail
else:
    print("Practical significance achieved.")
