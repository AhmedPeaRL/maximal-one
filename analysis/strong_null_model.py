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

    # 🔥 destroy long memory
    mix = np.diff(mix, prepend=mix[0])

    return mix
