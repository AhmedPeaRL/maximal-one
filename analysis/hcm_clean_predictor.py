import numpy as np

def hcm_clean_predict(history, predictors):

    if len(history) < 5:
        return history[-1]

    last = history[-1]

    # collect candidates
    candidates = []

    for p in predictors:
        try:
            val = float(p(history))
            if np.isfinite(val):
                candidates.append(val)
        except:
            continue

    if not candidates:
        return last

    # 🔥 remove persistence-like predictions
    non_trivial = [
        p for p in candidates
        if abs(p - last) > 1e-4
    ]

    if not non_trivial:
        return last

    # 🔥 score by directional consistency
    trend = np.sign(np.mean(np.diff(history[-5:])))

    def score(p):
        direction = np.sign(p - last)
        return -abs(p - last) + 0.5 * (direction == trend)

    best = max(non_trivial, key=score)

    return float(best)
