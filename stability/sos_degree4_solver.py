import sympy as sp
import cvxpy as cp
import numpy as np
from itertools import combinations_with_replacement

def monomial_basis(x, degree):
    n = len(x)
    basis = [1]
    for d in range(1, degree+1):
        for comb in combinations_with_replacement(range(n), d):
            term = 1
            for idx in comb:
                term *= x[idx]
            basis.append(term)
    return basis


def build_sos_program(f, degree=4):
    x = list(f.keys())
    z = monomial_basis(x, degree//2)

    m = len(z)
    Q = cp.Variable((m, m), symmetric=True)

    constraints = [Q >> 1e-6*np.eye(m)]

    # symbolic V
    V = 0
    for i in range(m):
        for j in range(m):
            V += Q[i,j]*z[i]*z[j]

    # substitute f(x)
    subs = {x[i]: f[x[i]] for i in range(len(x))}
    V_next = V.subs(subs)
    delta_V = sp.expand(V_next - V)

    # هنا نحتاج استخراج معاملات الحدود
    # للتحويل إلى قيود خطية
    # (يُستكمل بتوسيع coefficient matching)

    return Q, constraints
