import numpy as np

def invariant_break(history):

    h = np.array(history)

    if len(h) < 30:
        return history[-1]

    # 🔥 detect stagnation
    last_var = np.var(h[-10:])
    global_var = np.var(h)

    stagnation = last_var < 0.05 * global_var

    # 🔥 detect directional bias
    trend = np.mean(np.diff(h[-15:]))

    # 🔥 detect hidden acceleration
    accel = np.mean(np.gradient(np.gradient(h[-15:])))

    # 🔥 break condition
    if stagnation:

        jump = (
            1.5 * trend +
            0.8 * accel +
            np.random.normal(0, 0.2 * np.std(h))
        )

        return float(h[-1] + jump)

    return history[-1]
