import numpy as np

def generate_noise(n, seed=None):
    rng = np.random.default_rng(seed)
    return rng.normal(0, 1, n)

def inject_periodic(signal, amplitude=0.1, frequency=0.05):
    n = len(signal)
    t = np.arange(n)
    periodic = amplitude * np.sin(2 * np.pi * frequency * t)
    return signal + periodic
