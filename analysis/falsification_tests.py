import numpy as np

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.spectral_surrogate import phase_randomized_surrogate


def shuffle_test(series, rng):
    shuffled = rng.permutation(series)

    # فرق مهم: استخدم difference signal
    real_diff = np.diff(series)
    shuf_diff = np.diff(shuffled)

    a1 = estimate_alpha(real_diff)
    a2 = estimate_alpha(shuf_diff)

    return a2

def temporal_direction_test(series):
    forward = estimate_alpha(series)
    backward = estimate_alpha(series[::-1])
    return abs(forward - backward)

def phase_randomization(series, rng):
    surrogate = phase_randomized_surrogate(series, rng)
    return estimate_alpha(surrogate)


def white_noise_control(n, rng):
    wn = rng.standard_normal(n)
    return estimate_alpha(wn)


def run_falsification(series, rng):
    results = {}

    original_alpha = estimate_alpha(series)
    shuffled_alpha = shuffle_test(series, rng)
    phase_alpha = phase_randomization(series, rng)
    noise_alpha = white_noise_control(len(series), rng)

    values = {
        "original_alpha": original_alpha,
        "shuffled_alpha": shuffled_alpha,
        "phase_randomized_alpha": phase_alpha,
        "white_noise_alpha": noise_alpha
    }

    for key, value in values.items():

        if value is None:
            value = np.nan

        if not np.isfinite(value):
            # 🔥 controlled fallback بدل crash
            value = -1.0

        values[key] = float(value)

    results.update(values)

    return results
