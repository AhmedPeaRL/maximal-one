import numpy as np

def anti_collapse(history):

    if len(history) < 20:
        return history[-1]

    h = np.array(history[-20:])

    noise = np.std(h)
    drift = np.mean(np.diff(h))
    curvature = np.mean(np.abs(np.gradient(np.gradient(h))))

    exploration = (
        0.4 * drift +
        0.3 * curvature +
        np.random.normal(0, 0.2 * noise)
    )

    return float(history[-1] + exploration)
