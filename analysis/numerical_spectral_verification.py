import numpy as np

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
    for k in range(1, p):
        val = np.abs(np.sum(np.exp(2j*np.pi*k*seq/p)))/N
        if val > max_amp:
            max_amp = val
    return max_amp

if __name__ == "__main__":
    p = 10007
    a = 5
    N = 500

    seq = lcg_sequence(a, p, N)
    amp = spectral_amplitude(seq, p)

    print("Spectral amplitude:", amp)
    print("1/sqrt(N):", 1/np.sqrt(N))
