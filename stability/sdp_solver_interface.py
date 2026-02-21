import cvxpy as cp
import numpy as np

def solve_sdp(Q_matrix):
    n = Q_matrix.shape[0]
    P = cp.Variable((n,n), symmetric=True)

    constraints = [
        P >> 1e-6 * np.eye(n),
        Q_matrix.T @ P @ Q_matrix - P << -1e-6 * np.eye(n)
    ]

    prob = cp.Problem(cp.Minimize(0), constraints)
    prob.solve(solver=cp.SCS)

    return P.value
