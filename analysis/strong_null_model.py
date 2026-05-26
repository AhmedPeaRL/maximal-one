import numpy as np

def generate_strong_null(n, rng):
    wn = rng.standard_normal(n)

    # normalize
    wn = wn - np.mean(wn)
    wn = wn / (np.std(wn) + 1e-12)

    # 🔥 أقل عدوانية
    if rng.random() < 0.5:
        wn = np.diff(wn, prepend=wn[0])

    # 🔥 heavy phase randomization
    fft = np.fft.rfft(wn)
    phase = rng.uniform(0, 2*np.pi, len(fft))
    fft = np.abs(fft) * np.exp(1j * phase)

    x = np.fft.irfft(fft, n=n)

    # 🔥 inject anti-structure noise
    x += rng.normal(0, 1.0, n)
    x = np.diff(x, prepend=x[0])

    return x.astype(np.float64)
