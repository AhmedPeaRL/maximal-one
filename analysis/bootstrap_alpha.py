import json
import numpy as np
from .numerical_spectral_verification import estimate_alpha

np.random.seed(42)

def generate_powerlaw_series(n=1024, beta=1.0):
    freqs = np.fft.rfftfreq(n)
    freqs[0] = 1e-6

    spectrum = 1 / (freqs ** (beta / 2))
    phases = np.exp(2j * np.pi * np.random.rand(len(freqs)))

    signal = np.fft.irfft(spectrum * phases, n=n)
    return signal


series = generate_powerlaw_series(beta=1.0)

baseline_alpha = estimate_alpha(series)

boot = []
block_size = 32
num_boot = 50

for _ in range(num_boot):

    sample = []

    for _ in range(len(series) // block_size):
        start = np.random.randint(0, len(series) - block_size)
        sample.extend(series[start:start+block_size])

    sample = np.array(sample[:len(series)])

    boot.append(estimate_alpha(sample))

boot = np.array(boot)

result = {
    "baseline_alpha": float(baseline_alpha),
    "bootstrap_mean": float(np.mean(boot)),
    "bootstrap_std": float(np.std(boot)),
}

print(json.dumps(result, indent=2))
