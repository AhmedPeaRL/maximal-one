# analysis/nonlinear_phase_scan.py

import numpy as np
import matplotlib.pyplot as plt
import json
import os

np.random.seed(42)

# -----------------------------
# synthetic nonlinear generator
# -----------------------------

def generate_series(gamma, n=4000):

    x = np.zeros(n)
    x[0] = 0.5

    for t in range(1, n):
        x[t] = gamma * x[t-1] * (1 - x[t-1])

    return x


# -----------------------------
# spectral alpha estimator
# -----------------------------

def spectral_alpha(signal):

    signal = signal - np.mean(signal)

    fft = np.fft.rfft(signal)
    power = np.abs(fft) ** 2

    freqs = np.fft.rfftfreq(len(signal))

    mask = freqs > 0

    freqs = freqs[mask]
    power = power[mask]

    logf = np.log(freqs)
    logp = np.log(power)

    slope, _ = np.polyfit(logf, logp, 1)

    alpha = -slope

    return alpha


# -----------------------------
# phase scan
# -----------------------------

results = []

gammas = np.linspace(0.8, 1.0, 40)

for g in gammas:

    s = generate_series(g)

    a = spectral_alpha(s)

    results.append(
        {
            "gamma": float(g),
            "alpha": float(a)
        }
    )


# -----------------------------
# extract critical point
# -----------------------------

gamma_star = max(results, key=lambda x: x["alpha"])["gamma"]

alpha_star = max(r["alpha"] for r in results)

print("Critical gamma candidate:", gamma_star)
print("Alpha at critical:", alpha_star)


# -----------------------------
# save json result
# -----------------------------

os.makedirs("artifacts", exist_ok=True)

with open("artifacts/nonlinear_phase_scan.json", "w") as f:
    json.dump(
        {
            "gamma_star": gamma_star,
            "alpha_star": alpha_star,
            "scan_points": results
        },
        f,
        indent=2
    )


# -----------------------------
# plot
# -----------------------------

g = [r["gamma"] for r in results]
a = [r["alpha"] for r in results]

plt.figure(figsize=(6,4))
plt.plot(g, a)
plt.xlabel("gamma")
plt.ylabel("alpha")
plt.title("Nonlinear Phase Scan")

plt.tight_layout()

plt.savefig("artifacts/nonlinear_phase_transition.png")
