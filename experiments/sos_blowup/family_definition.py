import sympy as sp

x, y, eps = sp.symbols('x y eps')

def family_polynomial(epsilon):
    """
    Degenerate leading form at epsilon=0.
    Positive for epsilon>0.
    """
    return (
        x**4 * y**2
        + y**4 * x**2
        + epsilon * (x**6 + y**6)
        + 1
    )
