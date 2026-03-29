import numpy as np
from analysis.invariant_core import extract_invariants

class InvariantProjectionPredictor:

    def __init__(self, window=20):
        self.window = window

    def predict(self, history):
        
        if len(history) < self.window:
            return history[-1]
            
        h = np.array(history[-self.window:])
       
        inv = extract_invariants(h)
    
        if inv is None:
            return history[-1]

        energy, entropy, curvature, phase = inv

        # 🔥 dynamic weighting based on signal condition

        vol = np.std(h)
        trend = np.mean(np.diff(h))

        w_curv = 0.3 + 0.2 * np.tanh(vol)
        w_phase = 0.3 + 0.2 * np.tanh(abs(trend))
        w_entropy = 0.2
        w_energy = 0.2

        delta = (
            w_curv * curvature +
            w_phase * phase +
            w_entropy * entropy +
            w_energy * energy
        )

        return float(h[-1] + delta * np.std(h))
