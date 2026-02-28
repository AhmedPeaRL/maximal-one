import numpy as np
from numpy.linalg import eigvals

def main():
    rng = np.random.default_rng(42)
    A = np.array([[0.7, 0.2],
                  [-0.1, 0.85]])

    base = eigvals(A)

    perturb = rng.normal(scale=1e-5, size=A.shape)
    drift = eigvals(A + perturb)

    max_shift = np.max(np.abs(np.sort(base) - np.sort(drift)))

    print("Max eigenvalue drift:", max_shift)

    if max_shift > 1e-2:
        raise SystemExit("Eigen drift instability")

if __name__ == "__main__":
    main()
