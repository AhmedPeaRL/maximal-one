import numpy as np
from numpy.linalg import eigvals

def main():
    M = np.array([[0.8, 0.1],
                  [0.05, 0.9]])

    eigenvalues = eigvals(M)
    eigenvalues = sorted(abs(eigenvalues), reverse=True)

    gap = eigenvalues[0] - eigenvalues[1]

    print("Eigenvalues:", eigenvalues)
    print("Spectral gap:", gap)

    if gap <= 0:
        raise SystemExit("Spectral gap condition failed")

if __name__ == "__main__":
    main()
