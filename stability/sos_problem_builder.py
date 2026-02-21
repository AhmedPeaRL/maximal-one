import sympy as sp

def build_polynomial_system(dim, degree):
    x = sp.symbols(f'x0:{dim}')
    f = []

    for i in range(dim):
        expr = 0
        for j in range(dim):
            expr += 0.3 * x[j]  # stable linear core
        expr += -0.1 * x[i]**3  # nonlinear damping
        f.append(expr)

    return x, f


def candidate_lyapunov(x, degree=2):
    V = 0
    for xi in x:
        V += xi**2
    return V
