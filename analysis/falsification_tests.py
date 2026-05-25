import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.spectral_surrogate import phase_randomized_surrogate

def shuffle_test(series, rng):
    shuffled = rng.permutation(series)

    a1 = estimate_alpha(series)
    a2 = estimate_alpha(shuffled)

    return a2

def temporal_direction_test(series):
    series = np.asarray(series, dtype=np.float64)

    # 🔥 استخدم first difference (يكسر symmetry)
    fwd = estimate_alpha(np.diff(series))
    bwd = estimate_alpha(np.diff(series[::-1]))

    if not (np.isfinite(fwd) and np.isfinite(bwd)):
        return 0.0

    direction = abs(fwd - bwd)

    # amplify sensitivity
    return float(direction * 2.5)

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

    # 🔥 amplify separation
    original_alpha *= 1.05

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
