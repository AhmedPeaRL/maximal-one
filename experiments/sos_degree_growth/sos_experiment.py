import numpy as np
import cvxpy as cp

# ============================================
# Polynomial utilities (1D case only)
# ============================================

def monomial_vector(x, degree):
    return np.array([x**i for i in range(degree+1)])

# ============================================
# Generate polynomial coefficients
# ============================================

def generate_f_k(k, epsilon):
    # f_k(x) = (1 - x^2)^k + epsilon
    coeffs = np.zeros(2*k + 1)
    for i in range(k+1):
        coeff = (-1)**i * np.math.comb(k, i)
        coeffs[2*i] += coeff
    coeffs[0] += epsilon
    return coeffs

# ============================================
# SOS feasibility test
# ============================================

def sos_feasible(f_coeffs, max_deg):
    """
    Attempt Gram matrix SOS representation
    of degree <= max_deg
    """
    d = max_deg // 2
    Q = cp.Variable((d+1, d+1), PSD=True)

    # Build polynomial from Gram matrix
    coeffs = np.zeros(2*d+1)
    for i in range(d+1):
        for j in range(d+1):
            coeffs[i+j] += Q[i,j]

    constraints = []
    for i in range(len(f_coeffs)):
        if i < len(coeffs):
            constraints.append(coeffs[i] == f_coeffs[i])

    prob = cp.Problem(cp.Minimize(0), constraints)
    try:
        prob.solve(solver=cp.SCS, verbose=False)
        return prob.status == cp.OPTIMAL
    except:
        return False

# ============================================
# Main experiment
# ============================================

def run_experiment(k_values, epsilon, max_degree_search):
    results = []

    for k in k_values:
        f_coeffs = generate_f_k(k, epsilon)
        minimal_degree = None

        for deg in range(2, max_degree_search+1, 2):
            if sos_feasible(f_coeffs, deg):
                minimal_degree = deg
                break

        results.append((k, minimal_degree))
        print(f"k={k} -> minimal SOS degree = {minimal_degree}")

    return results

# ============================================

if __name__ == "__main__":
    k_values = [1,2,3,4,5,6,7,8]
    epsilon = 1e-4
    max_degree_search = 20

    run_experiment(k_values, epsilon, max_degree_search)
