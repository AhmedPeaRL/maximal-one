#!/usr/bin/env python3
"""
Invariant Layer: Guarantees "System Always Balances"
Robustness proof skeleton for bounded perturbations
"""

import numpy as np
from typing import Callable, List

class InvariantLayer:
    def __init__(self, state_dim: int, invariant_set: np.ndarray, 
                 admissible_perturbation: Callable[[np.ndarray], np.ndarray]):
        """
        state_dim: dimension of system state
        invariant_set: compact subset A
        admissible_perturbation: function generating allowed perturbations
        """
        self.state_dim = state_dim
        self.A = invariant_set
        self.perturb = admissible_perturbation

    def step(self, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Apply perturbation and project to invariant set if needed
        """
        dx = self.perturb(u)
        x_next = x + dx
        # Project to compact subset
        x_next = np.clip(x_next, self.A[:,0], self.A[:,1])
        return x_next

    def trajectory(self, x0: np.ndarray, inputs: List[np.ndarray]):
        traj = [x0]
        x = x0.copy()
        for u in inputs:
            x = self.step(x, u)
            traj.append(x)
        return np.array(traj)

    def check_invariant(self, traj: np.ndarray):
        """
        Verify that trajectory remains within compact subset and approaches A
        """
        in_bounds = np.all((traj >= self.A[:,0]) & (traj <= self.A[:,1]))
        converged = np.allclose(traj[-1], np.mean(self.A, axis=1), atol=1e-6)
        return in_bounds, converged
