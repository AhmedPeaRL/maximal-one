#!/usr/bin/env python3
"""
Define class of admissible perturbations
Robustness layer for theoretical validity
"""

import numpy as np

def bounded_noise(u: np.ndarray, eps: float = 0.01) -> np.ndarray:
    """
    Perturbation within bounds
    """
    delta = eps * (2*np.random.rand(*u.shape) - 1)
    return delta

def systematic_shift(u: np.ndarray, shift_factor: float = 0.05) -> np.ndarray:
    """
    Systematic shift perturbation
    """
    return u * shift_factor
