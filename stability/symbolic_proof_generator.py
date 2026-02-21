import sympy as sp

x1, x2 = sp.symbols('x1 x2')
V = x1**2 + x2**2

f1 = -x1 + x2**2
f2 = -x2

Vdot = sp.diff(V, x1)*f1 + sp.diff(V, x2)*f2
Vdot_simplified = sp.simplify(Vdot)

if __name__ == "__main__":
    print("Symbolic Vdot:")
    print(Vdot_simplified)
