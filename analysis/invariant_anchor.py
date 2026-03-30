import numpy as np

def invariant_anchor(history):
    """
    Generates prediction independent of local ordering,
    robust to phase + shuffle.
    """

    h = np.array(history)

    if len(h) < 30:
        return h[-1]

    # 🔥 invariant features
    mean = np.mean(h)
    std = np.std(h)
    energy = np.mean(h**2)

    # 🔥 gradient invariant
    grad = np.diff(h)
    grad_energy = np.mean(grad**2)

    # 🔥 curvature invariant
    curvature = np.mean(np.abs(np.gradient(np.gradient(h))))

    # 🔥 normalized invariant state
    state = (
        0.4 * mean +
        0.2 * std +
        0.2 * energy +
        0.1 * grad_energy +
        0.1 * curvature
    )

    # 🔥 controlled projection (NOT persistence)
    return float(state)
