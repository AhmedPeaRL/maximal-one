import numpy as np

class InvariantProjectionPredictor:

    def __init__(self, window=20):
        self.window = window

    def predict(self, history):

        if len(history) < self.window:
            return history[-1]

        h = np.array(history[-self.window:])

        # 🔥 normalize (remove scale bias)
        h_norm = (h - np.mean(h)) / (np.std(h) + 1e-8)

        # 🔥 local geometry
        grad = np.gradient(h_norm)
        curvature = np.gradient(grad)

        # 🔥 invariant direction (principal flow)
        direction = np.mean(grad[-5:])
        curvature_signal = np.mean(curvature[-5:])

        # 🔥 phase-consistent projection
        phase = np.sin(h_norm[-1])

        # 🔥 projected step
        delta = (
            0.5 * direction +
            0.3 * curvature_signal +
            0.2 * phase
        )

        # 🔥 return to original scale
        return float(h[-1] + delta * np.std(h))
