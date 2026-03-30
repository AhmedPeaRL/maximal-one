import numpy as np
from analysis.invariant_core_v2 import extract_strong_invariants

class InvariantDecoupledPredictor:

    def __init__(self, window=40):
        self.window = window

    def predict(self, history):

        if len(history) < self.window:
            return history[-1]

        h = np.array(history[-self.window:])

        inv = extract_strong_invariants(h)

        if inv is None:
            return history[-1]

        spec_energy, spec_entropy, rank_entropy, curvature, zero_cross = inv

        # 🔥 build invariant state (NO last value dependency)
        invariant_state = np.array([
            spec_entropy,
            rank_entropy,
            curvature,
            zero_cross
        ])

        # 🔥 project into signal space WITHOUT anchor
        scale = np.std(h) + 1e-8

        projection = (
            0.35 * invariant_state[0] +
            0.25 * invariant_state[1] +
            0.2 * invariant_state[2] +
            0.2 * invariant_state[3]
        )

        # 🔥 absolute reconstruction (NOT delta)
        base_level = np.mean(h)

        return float(base_level + projection * scale)
