import numpy as np
import math

def lcg_sequence(a, p, N):
    x = 1
    seq = []
    for _ in range(N):
        seq.append(x)
        x = (a * x) % p
    return np.array(seq)

def spectral_amplitude(seq, p):
    N = len(seq)
    max_amp = 0
    for k in range(1, min(p, 2000)):  # limit for computational feasibility
        val = abs(np.sum(np.exp(2j*np.pi*k*seq/p))) / N
        max_amp = max(max_amp, val)
    return max_amp

def verify_bound(p, a, N):
    seq = lcg_sequence(a, p, N)
    amp = spectral_amplitude(seq, p)

    theoretical_bound = 1 / math.sqrt(N)

    print("Prime p:", p)
    print("N:", N)
    print("Measured spectral amplitude:", amp)
    print("1/sqrt(N):", theoretical_bound)

    if amp <= 2 * theoretical_bound:
        print("BOUND_BEHAVIOR_CONFIRMED")
    else:
        print("BOUND_BEHAVIOR_VIOLATED")

if __name__ == "__main__":
    verify_bound(p=10007, a=5, N=500)
