import numpy as np

class SovereignInferenceEngine:
    def __init__(self):
        self.history = []
        self.state = "INIT"
        self.threshold = 0.15  # حساسية التغيير

    def ingest(self, alpha, noise_alpha):
        delta = abs(alpha - noise_alpha)

        signal = {
            "alpha": float(alpha),
            "noise_alpha": float(noise_alpha),
            "delta": float(delta)
        }

        self.history.append(signal)

        return self._decide(signal)

    def _decide(self, signal):
        if signal["delta"] > self.threshold:
            self.state = "STRUCTURE_DETECTED"
            return self._dispatch(signal)
        else:
            self.state = "NOISE_DOMINANT"
            return None

    def _dispatch(self, signal):
        return {
            "status": self.state,
            "confidence": signal["delta"],
            "action": "persist_structure"
        }

    def summary(self):
        if len(self.history) == 0:
            return None

        deltas = [h["delta"] for h in self.history]
        return {
            "mean_delta": float(np.mean(deltas)),
            "max_delta": float(np.max(deltas)),
            "state": self.state
        }
