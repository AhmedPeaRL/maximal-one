import numpy as np

def confidence_score(history):
    if len(history) < 30:
        return 0.0

    local_var = np.var(history[-20:])
    global_var = np.var(history)

    drift = abs(np.mean(np.diff(history[-10:])))
    noise = np.std(history[-20:])

    stability = 1 - (local_var / (global_var + 1e-8))

    signal_strength = drift / (noise + 1e-8)

    score = 0.5 * stability + 0.5 * signal_strength

    return float(np.clip(score, 0, 1))
