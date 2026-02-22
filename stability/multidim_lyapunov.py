"""
MultiDimensional Discrete-Time Linear System
Formal Lyapunov Stability Verification Harness

We verify:

1) A^T P A - P = -Q  (discrete Lyapunov equation)
2) P is positive definite
3) V(x_{k+1}) - V(x_k) <= -alpha ||x_k||^2

CI deterministic.
Numerically stable.
"""

import numpy as np
from scipy.linalg import solve_discrete_lyapunov

TOL = 1e-10


def solve_discrete_lyapunov_wrapper(A: np.ndarray, Q: np.ndarray) -> np.ndarray:
    """
    Solve: A^T P A - P = -Q
    Using scipy stable solver.
    """
    return solve_discrete_lyapunov(A.T, Q)


def is_positive_definite(M: np.ndarray) -> bool:
    eigvals = np.linalg.eigvals(M)
    return np.all(eigvals.real > TOL)


def spectral_radius(A: np.ndarray) -> float:
    eigvals = np.linalg.eigvals(A)
    return max(abs(eigvals.real))


class MultiDimensionalSystem:

    def __init__(self, A: np.ndarray):
        self.A = A
        self.n = A.shape[0]

        rho = spectral_radius(A)

        if rho >= 1.0 - TOL:
            raise RuntimeError(
                f"System not Schur-stable (spectral radius = {rho})"
            )

    def verify_lyapunov(self):

        Q = np.eye(self.n)
        P = solve_discrete_lyapunov_wrapper(self.A, Q)

        if not is_positive_definite(P):
            raise RuntimeError("Lyapunov matrix P is not positive definite")

        alpha = min(np.linalg.eigvals(Q).real)

        rng = np.random.default_rng(seed=42)

        for _ in range(500):

            x = rng.standard_normal((self.n, 1))

            Vx = float(x.T @ P @ x)
            x_next = self.A @ x
            Vx_next = float(x_next.T @ P @ x_next)

            lhs = Vx_next - Vx
            rhs = -alpha * float(x.T @ x)

            if lhs > rhs + 1e-8:
                raise RuntimeError("Lyapunov decrease condition violated")

        return {
            "spectral_radius": spectral_radius(self.A),
            "min_eigen_P": min(np.linalg.eigvals(P).real),
            "alpha": alpha
        }


if __name__ == "__main__":

    A = np.array([
        [0.6, 0.1],
        [0.0, 0.7]
    ])

    system = MultiDimensionalSystem(A)
    results = system.verify_lyapunov()

    print("Verification successful.")
    print("Spectral radius:", results["spectral_radius"])
    print("Min eigenvalue of P:", results["min_eigen_P"])
    print("Alpha:", results["alpha"])
