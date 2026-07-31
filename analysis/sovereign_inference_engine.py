import numpy as np

class SovereignInferenceEngine:
    def __init__(self):
        self.minimum_threshold = 0.15

    def adaptive_threshold(
        self,
        delta
    ):

        if not np.isfinite(delta):
            return self.minimum_threshold

        return float(
            max(
                self.minimum_threshold,
                round(delta * 0.05, 8)
            )
        )

    def ingest(
        self,
        alpha,
        noise_alpha
    ):

        alpha = float(alpha)
        noise_alpha = float(noise_alpha)

        delta = abs(
            alpha - noise_alpha
        )

        threshold = self.adaptive_threshold(
            delta
        )

        if delta > threshold:

            return {
                "status": "STRUCTURE_OBSERVED",
                "confidence": float(
                    round(delta, 8)
                ),
                "threshold": float(
                    round(threshold, 8)
                ),
                "action": "persist_structure"
            }

        return {
            "status": "NOISE_DOMINANT",
            "threshold": float(
                round(threshold, 8)
            )
        }

    def summary(
        self,
        alpha=None,
        noise_alpha=None
    ):

        if (
            alpha is None
            or noise_alpha is None
        ):
            return None

        delta = abs(
            float(alpha)
            - float(noise_alpha)
        )

        threshold = self.adaptive_threshold(
            delta
        )

        return {
            "mean_delta": float(
                round(delta, 8)
            ),
            "std_delta": 0.0,
            "max_delta": float(
                round(delta, 8)
            ),
            "adaptive_threshold": float(
                round(threshold, 8)
            ),
            "state": (
                "STRUCTURE_OBSERVED"
                if delta > threshold
                else "NOISE_DOMINANT"
            )
        }
