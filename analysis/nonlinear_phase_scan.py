#!/usr/bin/env python3
import numpy as np
import subprocess
import json
import matplotlib.pyplot as plt

gammas = np.linspace(0.5, 1.2, 40)
beta = 0.15

lyapunov_values = []

for g in gammas:
    cmd = [
        "python",
        "repro-core/nonlinear_kernel.py",
        "--gamma", str(g),
        "--beta", str(beta),
        "--seed", "42"
    ]
    output = subprocess.check_output(cmd)
    data = json.loads(output)
    lyapunov_values.append(data["lyapunov"])

plt.figure(figsize=(8,5))
plt.plot(gammas, lyapunov_values)
plt.axhline(0, linestyle="--")
plt.xlabel("gamma")
plt.ylabel("Lyapunov Exponent")
plt.title("Nonlinear Phase Scan")
plt.tight_layout()
plt.savefig("artifacts/nonlinear_phase_transition.png")
