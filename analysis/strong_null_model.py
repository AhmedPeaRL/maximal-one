import numpy as np

def generate_strong_null(n, rng):
    # random walk أخف
    rw = np.cumsum(rng.standard_normal(n)) * 0.5

    # periodic أضعف
    t = np.linspace(0, 6*np.pi, n)
    seasonal = 0.1 * np.sin(t)

    # noise أعلى
    noise = rng.normal(0, 1.2, n)

    return rw + seasonal + noise
