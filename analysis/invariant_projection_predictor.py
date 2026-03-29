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

        # 🔥 invariant-driven dynamics
        delta = (
            0.4 * curvature +
            0.3 * phase +
            0.2 * entropy +
            0.1 * energy
        )

        return float(h[-1] + delta * np.std(h))
