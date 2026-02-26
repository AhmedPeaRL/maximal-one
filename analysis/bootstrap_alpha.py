import json
import numpy as np

with open("artifacts/spectral_profile.json") as f:
    data = json.load(f)

amps = np.array(data["amplitudes"])
Nvals = np.array(data["N_values"])

# Fit log-log slope repeatedly on resampled data
alphas = []

for _ in range(500):
    idx = np.random.choice(len(amps), len(amps), replace=True)
    a = np.polyfit(np.log(Nvals[idx]), np.log(amps[idx]), 1)
    alphas.append(-a[0])

mean_alpha = np.mean(alphas)
std_alpha = np.std(alphas)

print("BOOTSTRAP_ALPHA_MEAN:", mean_alpha)
print("BOOTSTRAP_ALPHA_STD:", std_alpha)
