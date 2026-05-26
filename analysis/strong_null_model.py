import numpy as np

def generate_strong_null(n, rng):
    wn = rng.standard_normal(n)

    # normalize
    wn = wn - np.mean(wn)
    wn = wn / (np.std(wn) + 1e-12)

    # 🔥 destroy temporal correlation بالكامل
    wn = np.diff(wn, prepend=wn[0])

    # 🔥 heavy phase randomization
    fft = np.fft.rfft(wn)
    phase = rng.uniform(0, 2*np.pi, len(fft))
    fft = np.abs(fft) * np.exp(1j * phase)

    x = np.fft.irfft(fft, n=n)

    # 🔥 inject anti-structure noise
    x += rng.normal(0, 0.5, n)

    return x.astype(np.float64)
