import numpy as np
from sos_lyapunov_certificate import compute_lyapunov_certificate

def perturb_matrix(A, epsilon=1e-4):
    noise = np.random.default_rng(42).normal(scale=epsilon, size=A.shape)
    return A + noise

def main():
    A = np.array([[0.9, 0.1],
                  [-0.2, 0.8]])

    cert_original = compute_lyapunov_certificate(A)

    A_perturbed = perturb_matrix(A)
    cert_perturbed = compute_lyapunov_certificate(A_perturbed)

    diff = abs(cert_original - cert_perturbed)

    print("Original certificate:", cert_original)
    print("Perturbed certificate:", cert_perturbed)
    print("Difference:", diff)

    if diff > 1e-2:
        raise SystemExit("SOS robustness violated")

if __name__ == "__main__":
    main()
