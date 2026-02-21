import cvxpy as cp
import sympy as sp
import numpy as np
from family_definition import family_polynomial

def monomials_2d(r):
    x, y = sp.symbols('x y')
    monoms = []
    for i in range(r+1):
        for j in range(r+1-i):
            monoms.append(x**i * y**j)
    return monoms

def sos_feasible(epsilon, r):
    x, y = sp.symbols('x y')
    p = family_polynomial(epsilon)

    monoms = monomials_2d(r)
    m = len(monoms)

    Q = cp.Variable((m,m), symmetric=True)
    constraints = [Q >> 0]

    poly_expr = 0
    for i in range(m):
        for j in range(m):
            poly_expr += Q[i,j] * monoms[i] * monoms[j]

    poly_expr = sp.expand(poly_expr)

    P_poly = sp.Poly(poly_expr, x, y)
    target_poly = sp.Poly(p, x, y)

    for mon in P_poly.monoms():
        c_expr = P_poly.coeff_monomial(x**mon[0]*y**mon[1])
        c_target = target_poly.coeff_monomial(x**mon[0]*y**mon[1])
        constraints.append(c_expr == float(c_target))

    prob = cp.Problem(cp.Minimize(0), constraints)

    try:
        prob.solve(solver=cp.SCS, verbose=False)
        return prob.status
    except:
        return "failed"
