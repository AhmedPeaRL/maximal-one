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

    d_inv = abs(inv_pred - last)
    d_struct = abs(struct_pred - last)

    # 🔥 لو invariants قوية → override
    if d_inv > d_struct * 1.2:
        return float(inv_pred)

    # 🔥 لو structure أقوى بس مش trivial
    if d_struct > 1e-6:
        return float(0.6 * struct_pred + 0.4 * inv_pred)

    return float(inv_pred)
