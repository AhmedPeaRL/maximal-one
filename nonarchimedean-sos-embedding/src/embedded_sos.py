import cvxpy as cp
import sympy as sp
import numpy as np

# symbols
x, z = sp.symbols('x z')

# basis up to degree 3 (رفع الدرجة لتسهيل feasibility)
monomials = [
    1, x, z,
    x**2, x*z, z**2,
    x**3, x**2*z, x*z**2, z**3
]

m = len(monomials)

Q = cp.Variable((m, m), symmetric=True)
constraints = [Q >> 1e-8*np.eye(m)]

# build sigma0
sigma0 = 0
for i in range(m):
    for j in range(m):
        sigma0 += Q[i, j] * monomials[i] * monomials[j]

# target polynomial
target = 2*x**2*z

# algebraic constraint
h = z*(1 + x**4) - 1

sigma0_expanded = sp.expand(sigma0)
target_expanded = sp.expand(target)

poly_diff = sp.expand(sigma0_expanded - target_expanded)

vars_list = [x, z]
poly_obj = sp.Poly(poly_diff, vars_list)

coeffs = poly_obj.coeffs()

for c in coeffs:
    constraints.append(c == 0)

prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve(solver=cp.SCS)

print("Solver status:", prob.status)
