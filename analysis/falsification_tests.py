import numpy as np

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.spectral_surrogate import phase_randomized_surrogate


def shuffle_test(series, rng):
    shuffled = rng.permutation(series)
    return estimate_alpha(shuffled)


def phase_randomization(series, rng):
    surrogate = phase_randomized_surrogate(series, rng)
    return estimate_alpha(surrogate)


def white_noise_control(n, rng):
    wn = rng.randn(n)
    return estimate_alpha(wn)


def run_falsification(series, rng):
    results = {}

    original_alpha = estimate_alpha(series)
    shuffled_alpha = shuffle_test(series, rng)
    phase_alpha = phase_randomization(series, rng)
    noise_alpha = white_noise_control(len(series), rng)

    results["original_alpha"] = float(original_alpha)
    results["shuffled_alpha"] = float(shuffled_alpha)
    results["phase_randomized_alpha"] = float(phase_alpha)
    results["white_noise_alpha"] = float(noise_alpha)

    return results
