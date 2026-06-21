import numpy as np

def white_null(n, rng):
    x = rng.standard_normal(n)

    x = x - np.mean(x)
    x = x / (np.std(x) + 1e-12)

    return x.astype(np.float64)

def random_walk_null(n, rng):
    x = np.cumsum(
        rng.standard_normal(n)
    )

    x = x - np.mean(x)
    x = x / (np.std(x) + 1e-12)

    return x.astype(np.float64)

def phase_surrogate_null(n, rng):
    wn = rng.standard_normal(n)

    fft = np.fft.rfft(wn)

    phase = rng.uniform(
        0,
        2*np.pi,
        len(fft)
    )

    phase[0] = 0.0

    x = np.fft.irfft(
        np.abs(fft) * np.exp(1j * phase),
        n=n
    )

    x = x - np.mean(x)
    x = x / (np.std(x) + 1e-12)

    return x.astype(np.float64)

def ar1_null(n, rng, phi=None):
    if phi is None:
        phi = rng.uniform(0.6, 0.98)

    x = np.zeros(n, dtype=np.float64)

    eps = rng.standard_normal(n)

    for i in range(1, n):
        x[i] = phi * x[i - 1] + eps[i]

    x = (x - np.mean(x)) / (np.std(x) + 1e-12)

    return x

def generate_strong_null(n, rng):
    p = rng.random()

    if p < 0.20:
        return white_null(n, rng)

    elif p < 0.40:
        return random_walk_null(n, rng)

    elif p < 0.60:
        return phase_surrogate_null(n, rng)

    elif p < 0.80:
        return ar1_null(n, rng)

    else:
        x = np.cumsum(
            rng.standard_normal(n)
        )

        x += (
            0.5 *
            rng.standard_normal(n)
        )

        x = (
            x - np.mean(x)
        ) / (
            np.std(x) + 1e-12
        )

        return x.astype(
            np.float64
)
