import numpy as np

def generate_strong_null(n, rng):
    wn = rng.standard_normal(n)

    wn = wn - np.mean(wn)
    wn = wn / (np.std(wn) + 1e-12)

    # 🔥 فقط phase randomization (بدون تدمير كامل)
    fft = np.fft.rfft(wn)
    phase = rng.uniform(0, 2*np.pi, len(fft))
    phase[0] = 0.0

    x = np.fft.irfft(np.abs(fft) * np.exp(1j * phase), n=n)

    return x.astype(np.float64)
