import numpy as np


def phase_randomized_surrogate(series, rng):
    series = np.asarray(series, dtype=np.float64)

    n = len(series)

    fft = np.fft.rfft(series)

    magnitudes = np.abs(fft)
    phases = np.angle(fft)

    random_phases = rng.uniform(
        low=0,
        high=2*np.pi,
        size=len(phases)
    )

    random_phases[0] = phases[0]

    if n % 2 == 0:
        random_phases[-1] = phases[-1]

    new_fft = magnitudes * np.exp(1j * random_phases)

    surrogate = np.fft.irfft(new_fft, n=n)

    return surrogate
