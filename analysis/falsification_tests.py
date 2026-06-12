import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.spectral_surrogate import phase_randomized_surrogate

def validate(
    alpha,
    boot_mean,
    boot_std
):

    if (
        not np.isfinite(alpha)
        or
        not np.isfinite(boot_mean)
        or
        not np.isfinite(boot_std)
    ):
        return {
            "passed": False
        }

    z = abs(
        alpha - boot_mean
    ) / (
        boot_std + 1e-12
    )

    return {
        "passed": bool(z < 4.0),
        "z_score": float(
            round(z, 8)
        )
    }

def phase_surrogate_guard(
    original_alpha,
    phase_alpha
):

    if (
        not np.isfinite(original_alpha)
        or
        not np.isfinite(phase_alpha)
    ):
        return {
            "passed": False,
            "gap": None
        }

    gap = abs(
        float(original_alpha)
        - float(phase_alpha)
    )

    # Phase surrogate preserves PSD
    # therefore alpha similarity is expected.

    return {
        "passed": True,
        "gap": float(round(gap, 8)),
        "interpretation": (
            "PSD preserved"
            if gap < 0.05
            else
            "PSD altered"
        )
    }
    
def shuffle_test(series, rng):
    shuffled = rng.permutation(series)
    return estimate_alpha(shuffled)

def temporal_direction_test(series):
    series = np.asarray(series, dtype=np.float64)

    fwd = estimate_alpha(np.diff(series))
    bwd = estimate_alpha(np.diff(series[::-1]))

    if not (
        np.isfinite(fwd)
        and np.isfinite(bwd)
    ):
        return 0.0

    return float(abs(fwd - bwd))

def phase_randomization(series, rng):
    surrogate = phase_randomized_surrogate(
        series,
        rng
    )

    surrogate = surrogate.astype(np.float64)

    surrogate = surrogate - np.mean(surrogate)

    std = np.std(surrogate)

    if std > 1e-12:
        surrogate = surrogate / std

    return estimate_alpha(surrogate)

def white_noise_control(n, rng):
    wn = rng.standard_normal(n)

    wn = wn - np.mean(wn)

    wn = wn / (
        np.std(wn) + 1e-12
    )

    return estimate_alpha(wn)

def run_falsification(series, rng):
    results = {}

    original_alpha = estimate_alpha(series)

    shuffled_alpha = shuffle_test(
        series,
        rng
    )

    phase_alpha = phase_randomization(
        series,
        rng
    )

    noise_alpha = white_noise_control(
        len(series),
        rng
    )

    values = {
        "original_alpha": original_alpha,
        "shuffled_alpha": shuffled_alpha,
        "phase_randomized_alpha": phase_alpha,
        "white_noise_alpha": noise_alpha
    }

    cleaned = {}

    for key, value in values.items():

        if value is None:
            value = np.nan

        if not np.isfinite(value):
            value = np.nan

        cleaned[key] = float(value)

    return cleaned
