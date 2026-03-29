import numpy as np
from analysis.invariant_core_v2 import extract_strong_invariants

class InvariantProjectionPredictor:

    def __init__(self, window=20):
        self.window = window

    def predict(self, history):
        
        if len(history) < self.window:
            return history[-1]
            
        h = np.array(history[-self.window:])
       
        inv = extract_strong_invariants(h)
    
        if inv is None:
            return history[-1]

        spec_energy, spec_entropy, rank_entropy, curvature, zero_cross = inv

        # 🔥 dynamic weighting based on signal condition

        vol = np.std(h)
        trend = np.mean(np.diff(h))

        w_curv = 0.3 + 0.2 * np.tanh(vol)
        w_phase = 0.3 + 0.2 * np.tanh(abs(trend))
        w_entropy = 0.2
        w_energy = 0.2

        delta = (
            0.3 * spec_entropy +
            0.25 * rank_entropy +
            0.25 * curvature +
            0.2 * zero_cross
        )

        amplification = 1.5 + np.tanh(vol)
        
        return float(h[-1] + delta * np.std(h) * amplification)
