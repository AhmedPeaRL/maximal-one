import sympy as sp

# Symbolic linearization of feedback kernel

# Define symbolic variables
a, b = sp.symbols('a b', real=True)

# Simple 2D feedback operator approximation
J = sp.Matrix([[a, b],
               [-b, a]])

# Eigenvalues
eigs = J.eigenvals()

print("Jacobian:")
print(J)
print("\nEigenvalues:")
print(eigs)

# Spectral radius
lambda1 = list(eigs.keys())[0]
rho = sp.sqrt(sp.re(lambda1)**2 + sp.im(lambda1)**2)

print("\nSpectral radius (symbolic):")
print(rho)

# Power-law heuristic approximation
alpha = 2 * (1 - rho)

print("\nHeuristic alpha expression:")
print(alpha)
