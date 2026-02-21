import numpy as np


class LinearSystem:
    def __init__(self, A, B, M):
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.M = float(M)


class TheoreticalVerifier:
    def __init__(self, system: LinearSystem):
        self.system = system

    def verify(self):
        A = self.system.A
        B = self.system.B
        M = self.system.M

        spectral_radius_squared = np.linalg.norm(A)**2

        if spectral_radius_squared >= 1:
            return {
                "stable": False,
                "reason": "Spectral radius squared >= 1"
            }

        ultimate_bound = (np.linalg.norm(B)**2 * M**2) / (1 - spectral_radius_squared)

        return {
            "stable": True,
            "spectral_radius_squared": float(spectral_radius_squared),
            "ultimate_bound": float(ultimate_bound)
        }
