import numpy as np
from utils import generate_random_stable_matrix, lyapunov_certificate, is_schur_stable

def certify_family(dim=4, samples=100, alpha=1e-6):
    Q = np.eye(dim)
    failures = []

    for seed in range(samples):
        A = generate_random_stable_matrix(dim, seed)
        stable, rho = is_schur_stable(A)

        if not stable:
            failures.append(("unstable", seed))
            continue

        P, residual = lyapunov_certificate(A, Q)

        if not np.all(np.linalg.eigvals(P) > 0):
            failures.append(("P_not_positive_definite", seed))

        if residual > alpha:
            failures.append(("residual_too_large", seed))

    return failures

if __name__ == "__main__":
    failures = certify_family()
    if failures:
        raise RuntimeError(f"Certification failed: {failures}")
    print("Robust linear family certification passed.")
