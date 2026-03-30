import numpy as np
from analysis.invariant_core_v2 import extract_strong_invariants

def invariant_master_predict(history):

    if len(history) < 60:
        return history[-1]

    h = np.array(history[-40:])

    inv = extract_strong_invariants(h)

    if inv is None:
        return history[-1]

    spec_energy, spec_entropy, rank_entropy, curvature, zero_cross = inv

    # 🔥 invariants-only dynamics (NO TIME DEPENDENCE)

    scale = np.std(h) + 1e-8

    invariant_delta = (
        0.3 * spec_entropy +
        0.25 * rank_entropy +
        0.2 * curvature +
        0.15 * zero_cross
    )

    # 🔥 remove temporal bias
    drift = np.mean(np.diff(h))
    correction = -0.5 * drift

    return float(h[-1] + invariant_delta * scale + correction)
