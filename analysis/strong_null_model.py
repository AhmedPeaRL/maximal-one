import numpy as np

def generate_strong_null(n, rng):
    rw = np.cumsum(rng.standard_normal(n))

    t = np.linspace(0, 20*np.pi, n)
    seasonal = 0.3 * np.sin(t)

    noise = rng.normal(0, np.std(rw), n)

    mix = (
        0.4 * rw +
        0.2 * seasonal +
        0.4 * noise
    )

    return mix
