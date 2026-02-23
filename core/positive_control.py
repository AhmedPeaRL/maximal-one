import numpy as np

def inject_periodic_signal(data, amplitude=0.1, frequency=5, seed=42):
    """
    Injects a weak sinusoidal signal into noise.
    Used as positive control calibration layer.
    """
    rng = np.random.default_rng(seed)
    n = len(data)
    t = np.arange(n)

    signal = amplitude * np.sin(2 * np.pi * frequency * t / n)
    noise = data.copy()

    return noise + signal


def power_curve_test(detector_fn, n=1000000, amplitudes=None):
    """
    Runs detection power curve over amplitude ladder.
    """
    if amplitudes is None:
        amplitudes = np.linspace(0.01, 0.5, 10)

    results = []

    base_noise = np.random.normal(0, 1, n)

    for amp in amplitudes:
        test_data = inject_periodic_signal(base_noise, amplitude=amp)
        detected = detector_fn(test_data)
        results.append({
            "amplitude": float(amp),
            "detected": bool(detected)
        })

    return results
