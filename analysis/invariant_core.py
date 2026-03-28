import numpy as np

def extract_invariants(series):

    x = np.array(series)

    if len(x) < 50:
        return None

    # 🔥 normalize
    x = (x - np.mean(x)) / (np.std(x) + 1e-8)

    # 🔥 first derivative
    dx = np.gradient(x)

    # 🔥 second derivative
    ddx = np.gradient(dx)

    # 🔥 energy
    energy = np.mean(x**2)

    # 🔥 entropy approximation
    hist, _ = np.histogram(x, bins=20, density=True)
    hist = hist + 1e-8
    entropy = -np.sum(hist * np.log(hist))

    # 🔥 curvature invariant
    curvature = np.mean(np.abs(ddx))

    # 🔥 phase invariant
    phase = np.mean(np.sin(x))

    return np.array([
        energy,
        entropy,
        curvature,
        phase
    ])
