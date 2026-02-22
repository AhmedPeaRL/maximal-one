import cvxpy as cp
import numpy as np
import itertools
import json
from sympy import symbols, Poly, expand

x = symbols('x')

def monomial_vector(max_degree):
    return [x**i for i in range(max_degree + 1)]

def gram_sos_polynomial(Q, basis):
    n = len(basis)
    poly = 0
    for i in range(n):
        for j in range(n):
            poly += Q[i, j] * basis[i] * basis[j]
    return expand(poly)

def poly_to_coeff_vector(poly, max_degree):
    P = Poly(poly, x)
    coeffs = []
    for i in range(max_degree + 1):
        coeffs.append(float(P.coeff_monomial(x**i)))
    return np.array(coeffs)

def attempt_degree(k, d):
    f = expand((1 - x**2)**k)

    basis = monomial_vector(d)
    n = len(basis)

    Q0 = cp.Variable((n, n), PSD=True)
    Q1 = cp.Variable((n, n), PSD=True)

    sigma0 = gram_sos_polynomial(Q0, basis)
    sigma1 = gram_sos_polynomial(Q1, basis)

    candidate = expand(sigma0 + sigma1*(1 - x**2))

    max_deg = max(Poly(f, x).degree(), Poly(candidate, x).degree())

    f_vec = poly_to_coeff_vector(f, max_deg)
    c_vec = poly_to_coeff_vector(candidate, max_deg)

    constraints = [c_vec == f_vec]

    prob = cp.Problem(cp.Minimize(0), constraints)

    try:
        prob.solve(solver=cp.SCS, verbose=False)
        if prob.status in ["optimal", "optimal_inaccurate"]:
            return True
    except:
        pass

    return False

def scan_k(k, max_degree=10):
    for d in range(k, max_degree+1):
        feasible = attempt_degree(k, d)
        if feasible:
            return d
    return None

if __name__ == "__main__":
    results = {}
    for k in range(1,6):
        d = scan_k(k, max_degree=12)
        results[k] = d

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Scan complete:", results)
