from __future__ import annotations

import numpy as np

class SovereignInferenceEngine:
    """
    Diagnostic structure-observation layer.

    This component is NOT a scientific claim gate.

    It does not perform hypothesis testing.
    It does not infer causality.
    It does not infer consciousness.
    It does not infer HCM validity.
    It does not override the declared stochastic null.

    Its output is intentionally descriptive only.
    """

    def __init__(self):
        self.minimum_threshold = 0.15

    def adaptive_threshold(self, delta):
        """
        Retained only for backward compatibility.

        No adaptive threshold is used as scientific evidence.
        """

        if not np.isfinite(delta):
            return float(
                self.minimum_threshold
            )

        return float(
            self.minimum_threshold
        )

    def ingest(
        self,
        alpha,
        noise_alpha,
    ):
        alpha = float(alpha)
        noise_alpha = float(noise_alpha)

        if not (
            np.isfinite(alpha)
            and np.isfinite(noise_alpha)
        ):
            return {
                "status": "INVALID_DIAGNOSTIC_INPUT",
                "scientific_claim_authority": False,
                "scientific_role": "diagnostic_only",
            }

        delta = abs(
            alpha - noise_alpha
        )

        threshold = self.minimum_threshold

        if delta > threshold:
            status = "DESCRIPTIVE_STRUCTURE_DIAGNOSTIC"
            action = "persist_structure_as_diagnostic"
        else:
            status = "DESCRIPTIVE_NOISE_DIAGNOSTIC"
            action = "retain_without_structure_label"

        return {
            "status": status,
            "confidence": float(
                round(delta, 8)
            ),
            "threshold": float(
                threshold
            ),
            "action": action,
            "adaptive_threshold_used": False,
            "scientific_claim_authority": False,
            "scientific_role": "diagnostic_only",
        }

    def summary(
        self,
        alpha=None,
        noise_alpha=None,
    ):
        if (
            alpha is None
            or noise_alpha is None
        ):
            return None

        alpha = float(alpha)
        noise_alpha = float(noise_alpha)

        if not (
            np.isfinite(alpha)
            and np.isfinite(noise_alpha)
        ):
            return {
                "scientific_claim_authority": False,
                "scientific_role": "diagnostic_only",
                "valid": False,
            }

        delta = abs(
            alpha - noise_alpha
        )

        threshold = self.minimum_threshold

        return {
            "mean_delta": float(
                round(delta, 8)
            ),
            "std_delta": 0.0,
            "max_delta": float(
                round(delta, 8)
            ),
            "adaptive_threshold": float(
                threshold
            ),
            "adaptive_threshold_used": False,
            "state": (
                "DESCRIPTIVE_STRUCTURE_DIAGNOSTIC"
                if delta > threshold
                else "DESCRIPTIVE_NOISE_DIAGNOSTIC"
            ),
            "scientific_claim_authority": False,
            "scientific_role": "diagnostic_only",
        }
