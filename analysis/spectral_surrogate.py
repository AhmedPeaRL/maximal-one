import numpy as np

def phase_randomized_surrogate(series, rng):
    series = np.asarray(series, dtype=np.float64)
    n = len(series)

    fft = np.fft.rfft(series)
    magnitudes = np.abs(fft)

    # 🎯 Phase randomization (strong)
    random_phases = rng.uniform(0, 2*np.pi, len(fft))

    # preserve DC only
    random_phases[0] = 0.0
    if n % 2 == 0:
        random_phases[-1] = 0.0

    distortion = 1 + 0.2 * rng.standard_normal(len(magnitudes))
    distortion = np.clip(distortion, 0.05, 4.0)

    # 🔥 random drop heavy
    drop_mask = rng.uniform(0, 1, len(magnitudes)) < 0.5
    magnitudes[drop_mask] *= rng.uniform(0.01, 0.2)
    magnitudes = magnitudes * distortion

    new_fft = magnitudes * np.exp(1j * random_phases)

    surrogate = np.fft.irfft(new_fft, n=n)

    if not np.all(np.isfinite(surrogate)):
        raise ValueError("Invalid surrogate generated")

    return surrogate
