import cvxpy as cp
import sympy as sp
import numpy as np


def build_monomials(x, y, r):
    monoms = []
    for i in range(r + 1):
        for j in range(r + 1 - i):
            monoms.append(x**i * y**j)
    return monoms


def polynomial_coeff_dict(poly, x, y):
    P = sp.Poly(sp.expand(poly), x, y)
    coeffs = {}
    for mon in P.monoms():
        coeffs[mon] = float(P.coeffs()[P.monoms().index(mon)])
    return coeffs


def sos_feasibility(epsilon, r):
    x, y = sp.symbols('x y')

    # target polynomial
    p = x**4 + y**4 + epsilon*(x**2 + y**2) + 1

    monoms = build_monomials(x, y, r)
    m = len(monoms)

    Q = cp.Variable((m, m), symmetric=True)
    constraints = [Q >> 0]

    # Build symbolic SOS polynomial
    poly_expr = 0
    for i in range(m):
        for j in range(m):
            poly_expr += Q[i, j] * monoms[i] * monoms[j]

    poly_expr = sp.expand(poly_expr)

    # Extract coefficients
    target_coeffs = polynomial_coeff_dict(p, x, y)
    sos_poly = sp.Poly(poly_expr, x, y)

    for mon in sos_poly.monoms():
        coeff_expr = sos_poly.coeff_monomial(x**mon[0] * y**mon[1])
        target_value = target_coeffs.get(mon, 0.0)
        constraints.append(coeff_expr == target_value)

    prob = cp.Problem(cp.Minimize(0), constraints)

    try:
        prob.solve(solver=cp.SCS, verbose=False)
        return prob.status
    except Exception:
        return "failed"


if __name__ == "__main__":
    epsilons = [1e-1, 1e-2, 1e-3, 1e-4]

    for eps in epsilons:
        print("epsilon =", eps)
        for r in [2, 3, 4]:
            status = sos_feasibility(eps, r)
            print("  degree", r, "->", status)
