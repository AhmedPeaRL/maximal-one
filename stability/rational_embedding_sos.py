import cvxpy as cp
import sympy as sp
import numpy as np

# symbolic variables
x, z = sp.symbols('x z')

# polynomial basis (degree ≤ 2)
monomials = [1, x, z, x**2, x*z, z**2]
m = len(monomials)

# Gram matrix variable
Q = cp.Variable((m, m), symmetric=True)

# PSD constraint
constraints = [Q >> 1e-8 * np.eye(m)]

# Build sigma0 = m^T Q m symbolically
sigma0 = 0
for i in range(m):
    for j in range(m):
        sigma0 += Q[i, j] * monomials[i] * monomials[j]

# Algebraic constraint
h = z*(1 + x**4) - 1

# Target polynomial
target = 2*x**2*z

# Expand symbolic expressions
sigma0_expanded = sp.expand(sigma0)
target_expanded = sp.expand(target)

# Collect coefficients
vars_list = [x, z]
poly_diff = sp.expand(sigma0_expanded - target_expanded)

coeffs = sp.Poly(poly_diff, vars_list).coeffs()

# Enforce coefficient matching = 0
for c in coeffs:
    constraints.append(c == 0)

# Solve SDP
prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve(solver=cp.SCS)

print("Status:", prob.status)
