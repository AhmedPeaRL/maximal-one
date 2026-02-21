#!/usr/bin/env python3
"""
Harness for verifying theoretical validity
- Always Balanced
- Robust under admissible perturbations
- Trajectory remains in compact set
- Converges to invariant set
"""

import numpy as np
from invariant_layer import InvariantLayer
from perturbations import bounded_noise, systematic_shift

# Define invariant set A for d-dimensional system
d = 3
A = np.array([[0,1], [0,1], [0,1]])  # Compact subset for each state dimension

# Initial state
x0 = np.array([0.5, 0.5, 0.5])

# Define admissible perturbations
perturbations = [bounded_noise, systematic_shift]

# Create invariant layer for each perturbation
results = {}
for i, perturb in enumerate(perturbations):
    layer = InvariantLayer(state_dim=d, invariant_set=A, admissible_perturbation=perturb)
    inputs = [np.random.rand(d) for _ in range(100)]
    traj = layer.trajectory(x0, inputs)
    in_bounds, converged = layer.check_invariant(traj)
    results[f"perturb_{i}"] = {
        "in_bounds": in_bounds,
        "converged": converged
    }

# Theoretical validation report
for k,v in results.items():
    print(f"{k}: in_bounds={v['in_bounds']}, converged={v['converged']}")

# Save results for GitHub artifact
import json
with open("core-scientific/publication-gate/invariant_report.json","w") as f:
    json.dump(results, f, indent=4)

class DynamicalSystem:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def F(self, x, u):
        return self.A @ x + self.B @ u

class LyapunovVerifier:
    def __init__(self, P):
        self.P = P

    def V(self, x):
        return x.T @ self.P @ x

    def delta_V(self, system, x, u):
        x_next = system.F(x, u)
        return self.V(x_next) - self.V(x)

def simulate(system, verifier, x0, perturbations):
    x = x0
    history = []
    for u in perturbations:
        dv = verifier.delta_V(system, x, u)
        history.append(dv)
        x = system.F(x, u)
    return np.array(history)
