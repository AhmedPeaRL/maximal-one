import numpy as np

def generate_strong_null(n, rng):
    rw = np.cumsum(rng.standard_normal(n))

    t = np.linspace(0, 20*np.pi, n)
    seasonal = 0.3 * np.sin(t)

    noise = rng.normal(0, np.std(rw), n)

    mix = (
        0.6 * noise +   # dominant noise
        0.2 * rw +
        0.2 * seasonal
    )

    # 🔥 destroy structure aggressively
    mix = np.diff(mix, prepend=mix[0])
    mix = np.diff(mix, prepend=mix[0])  # double differencing

    # remove persistence
    mix = mix - 0.8 * np.roll(mix, 1)
    mix[0] = 0.0

    return mix
