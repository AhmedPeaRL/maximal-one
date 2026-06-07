import numpy as np

def phase_randomized_surrogate(series, rng):
    series = np.asarray(series, dtype=np.float64)
    n = len(series)
    fft = np.fft.rfft(series)
    amplitudes = np.abs(fft)
    phases = np.angle(fft)
    random_phases = rng.uniform(
        0,
        2*np.pi,
        len(phases)
    )
    random_phases[0] = phases[0]

    if n % 2 == 0:
        random_phases[-1] = phases[-1]

    surrogate_fft = amplitudes * np.exp(
        1j * random_phases
    )
    surrogate = np.fft.irfft(
        surrogate_fft,
        n=n
    )
    surrogate = surrogate.astype(np.float64)

    return surrogate
