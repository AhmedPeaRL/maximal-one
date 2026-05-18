import numpy as np

def generate_strong_null(n, rng):
    rw = np.cumsum(rng.standard_normal(n))

    t = np.linspace(0, 20*np.pi, n)
    seasonal = 0.3 * np.sin(t)

    noise = rng.normal(0, np.std(rw), n)

    # 🔥 أقوى
    mix = (
        0.6 * rw +
        0.3 * seasonal +
        0.3 * noise
    )

    return mix
