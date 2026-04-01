import numpy as np

def collapse_decision(history, candidates):

    if not candidates:
        return history[-1]

    last = history[-1]

    # 🔥 remove trivial قريب من persistence
    filtered = [
        p for p in candidates
        if abs(p - last) > 1e-4
    ]

    if not filtered:
        filtered = candidates

    # 🔥 compute directional momentum
    trend = np.mean(np.diff(history[-5:]))

    def score(p):
        # اتجاه + بعد عن trivial
        direction = np.sign(p - last)
        alignment = direction * np.sign(trend)
        distance = abs(p - last)

        return alignment * distance

    best = max(filtered, key=score)

    return float(best)
