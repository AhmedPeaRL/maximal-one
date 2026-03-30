import numpy as np

def enforce_information_divergence(history, pred):

    h = np.array(history)

    if len(h) < 30:
        return pred

    last = h[-1]

    # 🔥 detect trivial collapse
    deviation = abs(pred - last)

    local_std = np.std(h[-20:])
    global_std = np.std(h)

    # 🔥 if prediction too close → force divergence
    if deviation < 0.05 * (local_std + 1e-8):

        trend = np.mean(np.diff(h[-10:]))
        accel = np.mean(np.gradient(np.gradient(h[-10:])))

        noise = np.random.normal(0, 0.3 * local_std)

        forced = last + 1.2 * trend + 0.8 * accel + noise

        return float(forced)

    return pred
