import numpy as np

def irreversible_decision(history, candidates):

    if len(candidates) == 0:
        return history[-1]

    last = history[-1]

    # remove trivial predictions
    filtered = [
        c for c in candidates
        if abs(c - last) > 1e-6
    ]

    if len(filtered) == 0:
        # force divergence
        drift = np.mean(np.diff(history[-5:]))
        noise = np.std(history[-10:])
        return float(last + drift + np.random.normal(0, noise * 0.2))

    # score by directional commitment
    scores = []
    for c in filtered:
        direction = np.sign(c - last)
        momentum = np.mean(np.sign(np.diff(history[-5:])))
        alignment = direction * momentum
        scores.append(alignment)

    best_idx = int(np.argmax(scores))

    return float(filtered[best_idx])
