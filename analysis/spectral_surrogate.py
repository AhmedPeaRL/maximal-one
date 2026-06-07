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

def phase_surrogate_guard(
    original_alpha,
    phase_alpha
):

    if (
        not np.isfinite(original_alpha)
        or
        not np.isfinite(phase_alpha)
    ):
        return {
            "passed": False,
            "gap": None
        }

    gap = abs(
        float(original_alpha)
        - float(phase_alpha)
    )

    return {
        "passed": bool(gap >= 0.05),
        "gap": float(round(gap, 8))
    }
