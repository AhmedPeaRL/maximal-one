# analysis/numerical_spectral_verification.py

import numpy as np
import json
import os

# -----------------------------
# Deterministic LCG parameters
# -----------------------------
p = 2**31 - 1  # prime modulus
a = 48271      # Park-Miller multiplier
seed = 123456

max_N = 5000
k = 1  # frequency index

# -----------------------------
# Generate LCG sequence
# -----------------------------
def generate_lcg(n):
    x = seed
    seq = []
    for _ in range(n):
        x = (a * x) % p
        seq.append(x)
    return np.array(seq, dtype=np.int64)

# -----------------------------
# Spectral amplitude
# -----------------------------
def spectral_amplitude(xs):
    N = len(xs)
    angles = 2 * np.pi * k * xs / p
    exp_sum = np.exp(1j * angles).sum()
    return abs(exp_sum) / N

# -----------------------------
# Empirical exponent estimation
# -----------------------------
def estimate_exponent(N_values, amplitudes):
    logN = np.log(N_values)
    logA = np.log(amplitudes)
    slope, _ = np.polyfit(logN, logA, 1)
    return -slope  # since amplitude ~ N^{-alpha}

# -----------------------------
# Main profiling
# -----------------------------
N_values = np.unique(np.logspace(2, np.log10(max_N), 25).astype(int))
amplitudes = []

full_seq = generate_lcg(max_N)

for N in N_values:
    xs = full_seq[:N]
    amp = spectral_amplitude(xs)
    amplitudes.append(amp)

amplitudes = np.array(amplitudes)
alpha_est = estimate_exponent(N_values, amplitudes)

# -----------------------------
# Output artifacts
# -----------------------------
os.makedirs("artifacts", exist_ok=True)

profile = {
    "N_values": N_values.tolist(),
    "amplitudes": amplitudes.tolist(),
    "estimated_alpha": float(alpha_est),
    "reference_half": 0.5
}

with open("artifacts/spectral_profile.json", "w") as f:
    json.dump(profile, f, indent=2)

print("==== SPECTRAL PROFILE ====")
print(json.dumps(profile, indent=2))
