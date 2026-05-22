import numpy as np

def generate_strong_null(n, rng):
    rw = np.cumsum(rng.standard_normal(n))

    t = np.linspace(0, 20*np.pi, n)
    seasonal = 0.3 * np.sin(t)

    noise = rng.normal(0, np.std(rw), n)

    mix = (
        0.9 * noise +   # 🔥 noise أعلى
        0.05 * rw +
        0.05 * seasonal
    )

    mix = mix - np.mean(mix)
    mix = mix / (np.std(mix) + 1e-12)

    # 🔥 reduce over-destruction
    mix = mix - 0.6 * np.roll(mix, 1)  # 🔥 destroy persistence أكتر
    mix[0] = 0.0

    return mix
