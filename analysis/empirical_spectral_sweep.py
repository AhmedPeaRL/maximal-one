import numpy as np
import random
from numpy.fft import fft
import math


def spectral_max(seed, N):
    random.seed(seed)
    X = np.array([random.random() for _ in range(N)])
    F = fft(X) / N
    return np.max(np.abs(F[1:]))


def sweep(seeds, N_values):
    results = []
    for N in N_values:
        vals = []
        for s in seeds:
            vals.append(spectral_max(s, N))
        max_val = max(vals)
        results.append((N, max_val))
    return results


if __name__ == "__main__":
    seeds = range(2000)
    N_values = [256, 512, 1024, 2048, 4096, 8192]

    res = sweep(seeds, N_values)

    print("N, S_N, logN, logS_N")
    for N, v in res:
        print(
            N,
            v,
            math.log(N),
            math.log(v)
        )
