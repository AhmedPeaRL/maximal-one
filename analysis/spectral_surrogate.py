import numpy as np

def phase_randomized_surrogate(series, rng):
    series = np.asarray(series, dtype=np.float64)

    n = len(series)

    fft = np.fft.rfft(series)

    magnitudes = np.abs(fft)

    # 🔥 بدل random phases pure → نكسر coherence
    random_phases = rng.uniform(
        low=0,
        high=2*np.pi,
        size=len(fft)
    )

    # 🔥 نحافظ فقط على DC component
    random_phases[0] = 0.0

    if n % 2 == 0:
        random_phases[-1] = 0.0

    # 🔥 إدخال distortion طيفي بسيط
    magnitudes = magnitudes * (
        1 + 0.15 * rng.standard_normal(len(magnitudes))
    )

    new_fft = magnitudes * np.exp(1j * random_phases)

    surrogate = np.fft.irfft(new_fft, n=n)

    if not np.all(np.isfinite(surrogate)):
        raise ValueError("Invalid surrogate generated")

    return surrogate
