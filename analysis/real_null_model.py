import numpy as np
import pandas as pd
from analysis.numerical_spectral_verification import estimate_alpha

def generate_real_null(series):
    """
    Build null model from REAL data using phase randomization
    (destroys structure but preserves distribution)
    """
    fft = np.fft.fft(series)
    phases = np.angle(fft)
    magnitudes = np.abs(fft)

    random_phases = np.random.uniform(0, 2*np.pi, len(phases))
    new_fft = magnitudes * np.exp(1j * random_phases)

    surrogate = np.fft.ifft(new_fft).real
    return surrogate


def build_null_distribution(series, n=200):
    null_alphas = []

    for _ in range(n):
        surr = generate_real_null(series)
        alpha = estimate_alpha(surr)
        null_alphas.append(alpha)

    return np.array(null_alphas)
