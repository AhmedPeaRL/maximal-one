import sympy as sp
from sos_problem_builder import build_polynomial_system, candidate_lyapunov

def compute_delta_V(x, f, V):
    substitutions = {x[i]: f[i] for i in range(len(x))}
    V_next = V.subs(substitutions)
    delta_V = sp.simplify(V_next - V)
    return delta_V


def check_sos_candidate(delta_V):
    # Placeholder: in full implementation connect to SDP solver
    # Here we symbolically check if delta_V is negative definite quadratic form
    return delta_V
