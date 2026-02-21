"""
Direct SOS attempt for rational Lyapunov derivative.

System:
    x' = -x/(1+x^4)

Lyapunov:
    V = x^2

dV/dt = -2x^2/(1+x^4)

This script shows that the expression is not polynomial
and cannot be directly formulated as SOS without embedding.
"""

import sympy as sp

x = sp.symbols('x')

V = x**2
f = -x/(1+x**4)

dV = sp.diff(V, x) * f

print("dV/dt =", sp.simplify(dV))

if not sp.Poly(sp.simplify(dV*(1+x**4)), x).is_polynomial():
    print("Expression is not polynomial even after naive manipulation.")
else:
    print("Polynomial after clearing denominator, but domain constraints missing.")
