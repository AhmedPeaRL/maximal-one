import json
import numpy as np
from .numerical_spectral_verification import estimate_alpha

# Recompute spectral amplitudes deterministically
np.random.seed(42)

def generate_powerlaw_series(n=1024, beta=1.0):
    freqs = np.fft.rfftfreq(n)
    freqs[0] = 1e-6

    spectrum = 1 / (freqs ** (beta / 2))
    phases = np.exp(2j * np.pi * np.random.rand(len(freqs)))

    signal = np.fft.irfft(spectrum * phases, n=n)
    return signal

series = generate_powerlaw_series(beta=1.0)

# Compute baseline alpha
baseline_alpha = estimate_alpha(series)

# Bootstrap
boot = []
for _ in range(200):
    idx = np.random.choice(len(series), len(series), replace=True)
    sample = series[idx]
    boot.append(estimate_alpha(sample))

boot = np.array(boot)

result = {
    "baseline_alpha": float(baseline_alpha),
    "bootstrap_mean": float(np.mean(boot)),
    "bootstrap_std": float(np.std(boot)),
}

print(json.dumps(result, indent=2))
