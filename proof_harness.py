import numpy as np


class DynamicalSystem:
    def __init__(self, A=None, B=None):
        # Stable linear system by default
        self.A = A if A is not None else np.array([[0.8]])
        self.B = B if B is not None else np.array([[0.1]])

    def step(self, x, u):
        return self.A @ x + self.B @ u


class LyapunovVerifier:
    def __init__(self, system, M=0.5, steps=50):
        self.system = system
        self.M = M
        self.steps = steps

    def V(self, x):
        return float(x.T @ x)

    def verify(self):
        x = np.array([[1.0]])
        stable = True

        for i in range(self.steps):
            u = np.array([[np.random.uniform(-self.M, self.M)]])
            x_next = self.system.step(x, u)

            if self.V(x_next) > self.V(x) + 1e-6:
                stable = False

            x = x_next

        return {"stable": stable}
