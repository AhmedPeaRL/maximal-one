import numpy as np

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.block_shuffle_null import block_shuffle


DEFAULT_SEED = 42


def generate_real_null(
    series,
    rng,
):
    """
    Build a diagnostic null model from real data
    using phase randomization.

    This path is diagnostic-only.

    A local RNG is mandatory so repeated executions
    with the same declared seed are reproducible.
    """
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    fft = np.fft.fft(series)

    magnitudes = np.abs(fft)

    random_phases = rng.uniform(
        0.0,
        2.0 * np.pi,
        len(fft),
    )

    new_fft = (
        magnitudes
        * np.exp(1j * random_phases)
    )

    surrogate = np.fft.ifft(
        new_fft
    ).real

    return surrogate


def build_null_distribution(
    series,
    n=200,
    seed=DEFAULT_SEED,
):
    """
    Build the non-primary diagnostic null distribution.

    The diagnostic path is deterministic for a fixed
    seed and input series.

    This function must not be used as the canonical
    stochastic-null inference.
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
