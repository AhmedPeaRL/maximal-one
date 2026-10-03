from __future__ import annotations

import numpy as np

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.block_shuffle_null import block_shuffle


DEFAULT_SEED = 42
DEFAULT_BLOCK_SIZE = 50


def generate_real_null(
    series,
    rng,
):
    """
    Build a diagnostic phase-randomized null from real data.

    The supplied local RNG is mandatory so repeated executions
    with the same declared seed and input are reproducible.

    This path is diagnostic-only and is not the canonical
    primary stochastic-null inference.
    """
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        raise ValueError(
            "series must be one-dimensional"
        )

    if len(series) == 0:
        raise ValueError(
            "series must not be empty"
        )

    if not np.all(
        np.isfinite(series)
    ):
        raise ValueError(
            "series contains non-finite values"
        )

    if (
        rng is None
        or not hasattr(rng, "uniform")
    ):
        raise TypeError(
            "rng must be a numpy.random.Generator"
        )

    fft = np.fft.rfft(series)

    magnitudes = np.abs(fft)

    random_phases = rng.uniform(
        0.0,
        2.0 * np.pi,
        len(fft),
    )

    # Preserve the DC component exactly.
    random_phases[0] = 0.0

    # Preserve the Nyquist component for even-length series.
    if len(series) % 2 == 0:
        random_phases[-1] = 0.0

    new_fft = (
        magnitudes
        * np.exp(
            1j * random_phases
        )
    )

    surrogate = np.fft.irfft(
        new_fft,
        n=len(series),
    )

    return surrogate


def build_null_distribution(
    series,
    n=200,
    seed=DEFAULT_SEED,
):
    """
    Build the non-primary diagnostic null distribution.

    The diagnostic path is deterministic for a fixed seed and
    input series.

    This function must not be used as the canonical stochastic-null
    inference.
    """
    n = int(n)

    if n < 1:
        raise ValueError(
            "n must be >= 1"
        )

    seed = int(seed)

    rng = np.random.default_rng(
        seed
    )

    null_alphas = []

    for _ in range(n):

        if rng.random() < 0.8:
            surrogate = generate_real_null(
                series,
                rng,
            )

        else:
            surrogate = block_shuffle(
                series,
                rng=rng,
                block_size=DEFAULT_BLOCK_SIZE,
            )

        alpha = estimate_alpha(
            surrogate
        )

        if np.isfinite(alpha):
            null_alphas.append(
                float(alpha)
            )

    return np.asarray(
        null_alphas,
        dtype=np.float64,
    )
