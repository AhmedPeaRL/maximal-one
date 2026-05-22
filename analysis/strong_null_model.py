import numpy as np

def generate_strong_null(n, rng):
    wn = rng.standard_normal(n)

    # 🔥 white noise dominant
    wn = wn - np.mean(wn)
    wn = wn / (np.std(wn) + 1e-12)

    # 🔥 phase destroy بالكامل
    fft = np.fft.rfft(wn)
    phase = rng.uniform(0, 2*np.pi, len(fft))
    fft = np.abs(fft) * np.exp(1j * phase)

    x = np.fft.irfft(fft, n=n)

    return x.astype(np.float64)
