import numpy as np
import pandas as pd
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.block_shuffle_null import block_shuffle

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

        if np.random.rand() < 0.5:
            surr = generate_real_null(series)
        else:
            surr = block_shuffle(series)

        alpha = estimate_alpha(surr)
        null_alphas.append(alpha)

    return np.array(null_alphas)
