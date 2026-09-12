from __future__ import annotations
import numpy as np

def phase_randomized_surrogate(series, rng):
    """
    Fourier phase-randomized surrogate.

    The amplitude spectrum of the observed signal is preserved
    while Fourier phase relationships are randomized.

    This function is diagnostic infrastructure only.
    It must never be used to force agreement with the
    canonical estimator.
    """

    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        raise ValueError(
            "series must be one-dimensional"
        )

    n = len(series)

    if n < 256:
        raise ValueError(
            "series too short for phase-randomized surrogate"
        )

    if not np.all(
        np.isfinite(series)
    ):
        raise ValueError(
            "series contains non-finite values"
        )

    mean = np.mean(series)

    if not np.isfinite(mean):
        raise ValueError(
            "series mean is non-finite"
        )

    centered = (
        series - mean
    )

    std = np.std(centered)

    if not np.isfinite(std) or std < 1e-12:
        raise ValueError(
            "series is degenerate"
        )

    fft = np.fft.rfft(centered)

    if not np.all(
        np.isfinite(fft)
    ):
        raise ValueError(
            "FFT contains non-finite values"
        )

    amplitudes = np.abs(fft)

    random_phases = rng.uniform(
        0.0,
        2.0 * np.pi,
        len(amplitudes),
    )

    # Preserve DC component exactly.
    random_phases[0] = 0.0

    # For even n, Nyquist coefficient must remain real.
    if n % 2 == 0:
        random_phases[-1] = 0.0

    surrogate_fft = (
        amplitudes
        * np.exp(1j * random_phases)
    )

    surrogate = np.fft.irfft(
        surrogate_fft,
        n=n,
    )

    surrogate = np.asarray(
        surrogate,
        dtype=np.float64,
    )

    if not np.all(
        np.isfinite(surrogate)
    ):
        raise ValueError(
            "Invalid surrogate generated"
        )

    surrogate_mean = np.mean(
        surrogate
    )

    surrogate_std = np.std(
        surrogate
    )

    if (
        not np.isfinite(surrogate_mean)
        or not np.isfinite(surrogate_std)
        or surrogate_std < 1e-12
    ):
        raise ValueError(
            "Degenerate surrogate generated"
        )

    surrogate = (
        surrogate
        - surrogate_mean
    ) / surrogate_std

    return surrogate
