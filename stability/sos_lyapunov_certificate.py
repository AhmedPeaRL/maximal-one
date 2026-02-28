import numpy as np
import sympy as sp


def compute_lyapunov_certificate(A):
    """
    Compute a simple quadratic Lyapunov certificate
    V(x) = x^T P x
    where P solves discrete Lyapunov equation:
    A^T P A - P = -Q
    Here we use Q = I
    """

    A = np.array(A, dtype=float)
    Q = np.eye(A.shape[0])

    # Solve discrete Lyapunov equation numerically
    # P = sum_{k=0}^∞ (A^T)^k Q A^k
    P = np.zeros_like(A)
    Ak = np.eye(A.shape[0])

    for _ in range(50):
        P += Ak.T @ Q @ Ak
        Ak = A @ Ak

    # Return scalar certificate: trace(P)
    return float(np.trace(P))
