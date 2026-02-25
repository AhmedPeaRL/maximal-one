import numpy as np
import random
from numpy.fft import fft

def spectral_deviation(seed, N):
    random.seed(seed)
    X = np.array([random.random() for _ in range(N)])
    F = fft(X) / N
    mean = np.mean(X)
    return np.max(np.abs(F[1:] - mean))

def sweep(seeds, N_values):
    results = []
    for N in N_values:
        vals = []
        for s in seeds:
            vals.append(spectral_deviation(s, N))
        results.append((N, np.max(vals)))
    return results

if __name__ == "__main__":
    seeds = range(1000)
    N_values = [256, 512, 1024, 2048, 4096]
    res = sweep(seeds, N_values)
    for N, v in res:
        print(N, v)
