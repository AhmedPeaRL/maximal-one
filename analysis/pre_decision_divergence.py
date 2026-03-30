import numpy as np

def pre_decision_divergence(history):

    h = np.array(history)

    if len(h) < 40:
        return None

    last = h[-1]

    local = h[-20:]
    trend = np.mean(np.diff(local))
    accel = np.mean(np.gradient(np.gradient(local)))
    volatility = np.std(local)

    curvature = np.mean(np.abs(np.gradient(np.gradient(local))))

    # 🔥 detect flat / collapse regime
    flatness = np.std(np.diff(local))

    if flatness < 0.5 * volatility:
        # system pretending to be stable → force escape
        jump = (
            1.5 * trend +
            1.2 * accel +
            np.random.normal(0, 0.4 * volatility)
        )
        return float(last + jump)

    # 🔥 detect chaotic instability
    if curvature > volatility:
        jump = (
            0.8 * trend +
            1.5 * accel +
            np.random.normal(0, 0.6 * volatility)
        )
        return float(last + jump)

    return None
