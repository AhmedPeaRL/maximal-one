import numpy as np

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
