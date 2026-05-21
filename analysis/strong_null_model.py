import numpy as np

def generate_strong_null(n, rng):
    rw = np.cumsum(rng.standard_normal(n))

    t = np.linspace(0, 20*np.pi, n)
    seasonal = 0.3 * np.sin(t)

    noise = rng.normal(0, np.std(rw), n)

    mix = (
        0.8 * noise +   # 🔥 خلي noise dominant أكتر
        0.1 * rw +
        0.1 * seasonal
    )

    mix = np.diff(mix, prepend=mix[0])

    # 🔥 reduce over-destruction
    mix = mix - 0.3 * np.roll(mix, 1)
    mix[0] = 0.0

    return mix
