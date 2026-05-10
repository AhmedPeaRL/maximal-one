import numpy as np


class SovereignInferenceEngine:

    def __init__(self):

        self.history = []

        self.state = "INIT"

        self.minimum_threshold = 0.15

    def adaptive_threshold(self):

        if len(self.history) < 5:
            return self.minimum_threshold

        deltas = np.array([
            h["delta"]
            for h in self.history
        ])

        mean = np.mean(deltas)
        std = np.std(deltas)

        adaptive = mean + (0.5 * std)

        return max(
            self.minimum_threshold,
            float(adaptive)
        )

    def ingest(
        self,
        alpha,
        noise_alpha
    ):

        delta = abs(
            alpha - noise_alpha
        )

        signal = {
            "alpha": float(alpha),
            "noise_alpha": float(noise_alpha),
            "delta": float(delta)
        }

        self.history.append(signal)

        return self._decide(signal)

    def _decide(
        self,
        signal
    ):

        threshold = self.adaptive_threshold()

        if signal["delta"] > threshold:

            self.state = (
                "STRUCTURE_DETECTED"
            )

            return self._dispatch(
                signal,
                threshold
            )

        self.state = "NOISE_DOMINANT"

        return {
            "status": self.state,
            "threshold": threshold
        }

    def _dispatch(
        self,
        signal,
        threshold
    ):

        return {
            "status": self.state,
            "confidence": signal["delta"],
            "threshold": threshold,
            "action": "persist_structure"
        }

    def summary(self):

        if len(self.history) == 0:
            return None

        deltas = np.array([
            h["delta"]
            for h in self.history
        ])

        return {
            "mean_delta": float(
                np.mean(deltas)
            ),
            "std_delta": float(
                np.std(deltas)
            ),
            "max_delta": float(
                np.max(deltas)
            ),
            "adaptive_threshold":
                self.adaptive_threshold(),
            "state": self.state
        }
