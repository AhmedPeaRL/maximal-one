import numpy as np
from analysis.invariant_core_v2 import extract_strong_invariants

def invariant_resilience_score(history, pred):

    if len(history) < 60:
        return 1.0  # neutral

    h = np.array(history[-40:])

    base_inv = extract_strong_invariants(h)
    if base_inv is None:
        return 1.0

    simulated = np.append(h, pred)[-40:]
    pred_inv = extract_strong_invariants(simulated)

    if pred_inv is None:
        return 1.0

    dist = np.linalg.norm(base_inv - pred_inv)

    # 🔥 normalize into resilience score
    score = np.exp(-dist)

    return float(score)


def enforce_invariant_resilience(history, pred):

    score = invariant_resilience_score(history, pred)

    last = history[-1]

    # 🔥 لو prediction كسر invariants بشدة → نرجّعه
    if score < 0.6:
        correction = 0.7 * (last - pred)
        return float(pred + correction)

    # 🔥 لو متوسط → نهدّيه
    if score < 0.8:
        return float(0.5 * pred + 0.5 * last)

    return float(pred)
