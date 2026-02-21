import numpy as np
from numpy.linalg import eigvals
from scipy.linalg import solve_discrete_lyapunov

def is_schur_stable(A):
    rho = max(abs(eigvals(A)))
    return rho < 1.0, rho

def generate_random_stable_matrix(dim, seed):
    rng = np.random.default_rng(seed)
    M = rng.normal(size=(dim, dim))
    u, _, vh = np.linalg.svd(M)
    radius = rng.uniform(0.2, 0.9)
    return radius * (u @ vh)

def lyapunov_certificate(A, Q):
    P = solve_discrete_lyapunov(A, Q)
    residual = A.T @ P @ A - P + Q
    return P, np.linalg.norm(residual)
