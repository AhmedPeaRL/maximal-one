import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha


def shuffle_test(series):
    shuffled = np.random.permutation(series)
    return estimate_alpha(shuffled)


def phase_randomization(series):
    fft = np.fft.rfft(series)
    phases = np.angle(fft)
    magnitudes = np.abs(fft)

    random_phases = np.random.uniform(0, 2*np.pi, len(phases))
    new_fft = magnitudes * np.exp(1j * random_phases)

    new_series = np.fft.irfft(new_fft)
    return estimate_alpha(new_series)


def white_noise_control(n):
    wn = np.random.randn(n)
    return estimate_alpha(wn)


def run_falsification(series):
    results = {}

    results["original_alpha"] = estimate_alpha(series)
    results["shuffled_alpha"] = shuffle_test(series)
    results["phase_randomized_alpha"] = phase_randomization(series)
    results["white_noise_alpha"] = white_noise_control(len(series))

    return results
