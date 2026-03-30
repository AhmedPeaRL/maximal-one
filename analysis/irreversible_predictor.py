import numpy as np

def irreversible_signal(history):
    """
    Extract directional signal that survives chaos.
    """

    h = np.array(history)

    if len(h) < 20:
        return h[-1]

    # 🔥 local velocity
    velocity = np.mean(np.diff(h[-5:]))

    # 🔥 acceleration
    accel = np.mean(np.diff(np.diff(h[-5:])))

    # 🔥 asymmetry (time directionality)
    forward = np.mean(h[-5:])
    backward = np.mean(h[-10:-5])

    asymmetry = forward - backward

    # 🔥 directional energy
    energy = np.sum(np.sign(np.diff(h[-10:])))

    signal = (
        0.4 * velocity +
        0.3 * accel +
        0.2 * asymmetry +
        0.1 * energy
    )

    return float(signal)


def irreversible_predict(history, anchor):

    signal = irreversible_signal(history)

    # 🔥 controlled injection
    return float(anchor + 0.5 * signal)
