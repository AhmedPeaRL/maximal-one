import numpy as np
from proof_harness import DynamicalSystem, LyapunovVerifier
from theoretical_guard import verify_monotonic_decrease, bounded_input_check

A = np.array([[0.9, 0.0],
              [0.0, 0.8]])

B = np.eye(2)
P = np.eye(2)

system = DynamicalSystem(A, B)
verifier = LyapunovVerifier(P)

x0 = np.array([1.0, 1.0])

np.random.seed(42)
perturbations = np.random.uniform(-0.05, 0.05, (200, 2))

assert bounded_input_check(perturbations, M=0.1), "Input not bounded"

history = simulate(system, verifier, x0, perturbations)

assert verify_monotonic_decrease(history), "Lyapunov not decreasing"

print("Theoretical stability verified.")
