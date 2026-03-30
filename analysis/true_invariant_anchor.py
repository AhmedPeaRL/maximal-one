import numpy as np

def true_invariant_anchor(history):
    """
    TRUE invariant anchor:
    invariant to phase, shuffle, and nonlinear distortions
    """

    h = np.array(history)

    if len(h) < 50:
        return float(h[-1])

    # 🔥 normalize (remove scale + shift)
    h = (h - np.mean(h)) / (np.std(h) + 1e-8)

    # 🔥 pairwise distance matrix (ORDER-INVARIANT)
    D = np.abs(h[:, None] - h[None, :])

    # 🔥 invariant signature
    signature = np.mean(D) + np.std(D)

    # 🔥 temporal roughness invariant
    diff = np.diff(h)
    roughness = np.mean(np.abs(diff))

    # 🔥 entropy-like invariant
    hist, _ = np.histogram(h, bins=20, density=True)
    hist = hist + 1e-8
    entropy = -np.sum(hist * np.log(hist))

    state = (
        0.4 * signature +
        0.3 * roughness +
        0.3 * entropy
    )

    return float(np.tanh(state))
