import numpy as np

def anti_persistence_force(history, pred):

    last = history[-1]

    # distance from persistence
    delta = pred - last

    # 🔥 if too close → FORCE divergence
    if abs(delta) < 1e-4:

        trend = np.mean(np.diff(history[-10:]))

        # curvature
        curvature = np.mean(np.gradient(np.gradient(history[-10:])))

        # noise-aware scaling
        noise = np.std(history[-20:]) + 1e-8

        forced = last + (0.5 * trend + 0.3 * curvature) * (1 + noise)

        return float(forced)

    return float(pred)
