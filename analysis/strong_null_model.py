import numpy as np

def generate_strong_null(n, rng):
    """
    Harder null:
    mixture of random walk + seasonal + noise
    """

    # base random walk
    rw = np.cumsum(rng.standard_normal(n))

    # add periodic component
    t = np.linspace(0, 10*np.pi, n)
    seasonal = 0.5 * np.sin(t)

    # add noise
    noise = rng.normal(0, np.std(rw)*0.5, n)

    return rw + seasonal + noise
