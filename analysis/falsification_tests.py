import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha


def shuffle_test(series, rng):
    shuffled = rng.permutation(series)
    return estimate_alpha(shuffled)


def phase_randomization(series, rng):
    fft = np.fft.rfft(series)

    phases = np.angle(fft)
    magnitudes = np.abs(fft)

    random_phases = rng.uniform(0, 2*np.pi, len(phases))

    new_fft = magnitudes * np.exp(1j * random_phases)

    new_series = np.fft.irfft(new_fft)
    return estimate_alpha(new_series)


def white_noise_control(n, rng):
    wn = rng.randn(n)
    return estimate_alpha(wn)


def run_falsification(series, rng):
    results = {}

    results["original_alpha"] = float(estimate_alpha(series))
    results["shuffled_alpha"] = float(shuffle_test(series, rng))
    results["phase_randomized_alpha"] = float(phase_randomization(series, rng))
    results["white_noise_alpha"] = float(white_noise_control(len(series), rng))

    return results
