import numpy as np
from analysis.invariant_core_v2 import extract_strong_invariants

def invariant_projection(history):

    h = np.array(history[-30:])

    inv = extract_strong_invariants(h)

    if inv is None:
        return history[-1]

    spec_energy, spec_entropy, rank_entropy, curvature, zero_cross = inv

    vol = np.std(h)
    trend = np.mean(np.diff(h))

    # 🔥 invariant-driven delta
    delta = (
        0.25 * spec_entropy +
        0.25 * rank_entropy +
        0.2 * curvature +
        0.15 * zero_cross +
        0.15 * np.tanh(vol)
    )

    return float(h[-1] + delta * vol)


def blend(inv_pred, struct_pred, history):

    last = history[-1]

    # distance from persistence
    d_inv = abs(inv_pred - last)
    d_struct = abs(struct_pred - last)

    # 🔥 enforce anti-triviality
    w_inv = d_inv + 1e-8
    w_struct = d_struct + 1e-8

    weights = np.array([w_inv, w_struct])
    weights /= np.sum(weights)

    return float(weights[0] * inv_pred + weights[1] * struct_pred)
