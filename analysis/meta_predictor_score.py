import json

with open("artifacts/lorenz.json") as f:
    d = json.load(f)

score = (d["mse_naive"] - d["mse_hcm"]) / d["mse_naive"]

print("Meta Predictive Score:", score)

if score < 0:
    raise SystemExit("Negative predictive edge detected.")
