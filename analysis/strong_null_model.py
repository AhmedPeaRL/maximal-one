from __future__ import annotations
import numpy as np

def _normalize(x):
    x = np.asarray(
        x,
        dtype=np.float64,
    )

    x = x - np.mean(x)

    std = np.std(x)

    if std < 1e-12:
        return np.zeros_like(x)

    return x / std

def white_null(n, rng):
    x = rng.standard_normal(n)
    return _normalize(x)

def random_walk_null(n, rng):
    x = np.cumsum(
        rng.standard_normal(n)
    )

    return _normalize(x)

def ar1_null(n, rng, phi=0.5):
    phi = float(phi)

    if not (-0.99 < phi < 0.99):
        raise ValueError(
            "AR1 phi must be inside (-0.99, 0.99)"
        )

    x = np.zeros(
        n,
        dtype=np.float64,
    )

    eps = rng.standard_normal(n)

    innovation_scale = np.sqrt(
        max(
            1.0 - phi * phi,
            1e-12,
        )
    )

    for i in range(1, n):
        x[i] = (
            phi * x[i - 1]
            + innovation_scale * eps[i]
        )

    return _normalize(x)

def block_shuffle_null(
    series,
    rng,
    block_size=32,
):
    """
    Shuffle blocks of the observed series.

    This preserves local within-block structure while
    destroying long-range ordering.
    """

    x = np.asarray(
        series,
        dtype=np.float64,
    ).copy()

    n = len(x)

    if n < block_size * 2:
        return _normalize(x[::-1])

    blocks = [
        x[i:i + block_size]
        for i in range(
            0,
            n,
            block_size,
        )
    ]

    rng.shuffle(blocks)

    return _normalize(
        np.concatenate(blocks)[:n]
    )

def phase_surrogate_null(
    series,
    rng,
):
    """
    Fourier phase-randomized surrogate.

    Crucially, the amplitude spectrum is taken from
    the OBSERVED series, not from independent white noise.

    Therefore the surrogate approximately preserves the
    observed power spectrum while destroying Fourier phase
    relationships.
    """

    x = np.asarray(
        series,
        dtype=np.float64,
    )

    if x.ndim != 1:
        raise ValueError(
            "series must be one-dimensional"
        )

    if len(x) < 256:
        raise ValueError(
            "series too short for phase surrogate"
        )

    x = x - np.mean(x)

    fft = np.fft.rfft(x)

    magnitude = np.abs(fft)

    phase = rng.uniform(
        0.0,
        2.0 * np.pi,
        len(fft),
    )

    # Preserve DC component.
    phase[0] = 0.0

    # For even n, Nyquist component must remain real.
    if len(x) % 2 == 0:
        phase[-1] = 0.0

    surrogate_fft = (
        magnitude
        * np.exp(1j * phase)
    )

    surrogate = np.fft.irfft(
        surrogate_fft,
        n=len(x),
    )

    return _normalize(surrogate)

def generate_strong_null(
    n,
    rng,
    mode="mixed",
    observed_series=None,
):
    """
    Generate null data.

    mode:
      - white
      - ar1
      - random_walk
      - block_shuffle
      - phase
      - mixed

    The mixed mode is a robustness ensemble and MUST NOT
    be interpreted as a single uniquely defined null
    hypothesis.
    """

    if mode == "white":
        return white_null(n, rng)

    if mode == "ar1":
        return ar1_null(n, rng)

    if mode == "random_walk":
        return random_walk_null(n, rng)

    if mode == "block_shuffle":
        if observed_series is None:
            raise ValueError(
                "observed_series required for block_shuffle"
            )

        return block_shuffle_null(
            observed_series,
            rng,
        )

    if mode == "phase":
        if observed_series is None:
            raise ValueError(
                "observed_series required for phase surrogate"
            )

        return phase_surrogate_null(
            observed_series,
            rng,
        )

    if mode == "mixed":
        p = rng.random()

        if p < 0.25:
            return white_null(n, rng)

        if p < 0.50:
            return ar1_null(n, rng)

        if p < 0.75:
            if observed_series is not None:
                return block_shuffle_null(
                    observed_series,
                    rng,
                )

            return random_walk_null(n, rng)

        if observed_series is not None:
            return phase_surrogate_null(
                observed_series,
                rng,
            )

        return white_null(n, rng)

    raise ValueError(
        f"Unknown null mode: {mode}"
    )
