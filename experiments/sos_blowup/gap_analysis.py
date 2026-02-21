import numpy as np
import sympy as sp
from family_definition import family_polynomial

x, y = sp.symbols('x y')

def compute_gap(epsilon, samples=5000):
    p = family_polynomial(epsilon)
    p_func = sp.lambdify((x, y), p, 'numpy')

    thetas = np.linspace(0, 2*np.pi, samples)
    values = []

    for t in thetas:
        xx = np.cos(t)
        yy = np.sin(t)
        values.append(p_func(xx, yy))

    return np.min(values)
