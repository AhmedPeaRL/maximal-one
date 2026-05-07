import numpy as np

from analysis.numerical_spectral_verification import (
    estimate_alpha
)


def generate_surrogate(series, rng):
    """
    Phase randomized surrogate
    preserves power spectrum
    destroys temporal structure
    """

    series = np.asarray(series, dtype=np.float64)

    fft = np.fft.rfft(series)

    random_phases = np.exp(
        1j * rng.uniform(
            0,
            2 * np.pi,
            len(fft)
        )
    )

    # preserve DC component
    random_phases[0] = 1.0

    new_fft = np.abs(fft) * random_phases

    surrogate = np.fft.irfft(
        new_fft,
        n=len(series)
    )

    surrogate = np.asarray(
        surrogate,
        dtype=np.float64
    )

    return surrogate


def run_null_test(real_series, n=32):

    rng = np.random.RandomState(42)

    real_alpha = estimate_alpha(real_series)

    if not np.isfinite(real_alpha):
        raise RuntimeError(
            "Real alpha invalid"
        )

    null_alphas = []

    for _ in range(n):

        surrogate = generate_surrogate(
            real_series,
            rng
        )

        a = estimate_alpha(surrogate)

        if np.isfinite(a):
            null_alphas.append(a)

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    if len(null_alphas) < 8:

        return {
            "real_alpha": float(real_alpha),
            "null_mean": np.nan,
            "null_std": np.nan,
            "z_score": np.nan,
            "pass": False,
            "reason": "insufficient_null_samples"
        }

    mean_null = float(np.mean(null_alphas))
    std_null = float(np.std(null_alphas))

    z_score = (
        (real_alpha - mean_null)
        / (std_null + 1e-8)
    )

    print("Real alpha:", real_alpha)
    print("Null mean:", mean_null)
    print("Null std:", std_null)
    print("Z-score:", z_score)
    print("Valid null samples:", len(null_alphas))

    passed = (
        np.isfinite(z_score)
        and z_score > 2.0
    )

    return {
        "real_alpha": float(real_alpha),
        "null_mean": mean_null,
        "null_std": std_null,
        "z_score": float(z_score),
        "pass": bool(passed),
        "valid_samples": int(len(null_alphas))
    }
