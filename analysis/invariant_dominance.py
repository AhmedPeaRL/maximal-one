import numpy as np
from analysis.invariant_core_v2 import extract_strong_invariants

def invariant_distance(inv1, inv2):
    return np.linalg.norm(inv1 - inv2)

def invariant_guard(history, pred):

    if len(history) < 50:
        return pred

    h = np.array(history[-30:])

    base_inv = extract_strong_invariants(h)

    if base_inv is None:
        return pred

    # simulate candidate
    simulated = np.append(h, pred)[-30:]
    pred_inv = extract_strong_invariants(simulated)

    if pred_inv is None:
        return pred

    dist = invariant_distance(base_inv, pred_inv)

    # 🔥 لو prediction كسر الـ invariants → نعاقبه
    if dist > 0.5:
        correction = -0.5 * (pred - history[-1])
        return float(pred + correction)

    return float(pred)
