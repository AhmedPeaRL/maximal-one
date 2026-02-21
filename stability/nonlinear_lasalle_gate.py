import numpy as np

def nonlinear_system(x):
    return np.array([
        -x[0] + x[1]**2,
        -x[1]
    ])

def lyapunov_function(x):
    return x[0]**2 + x[1]**2

def lasalle_check(samples=500):
    for i in range(samples):
        x = np.random.uniform(-1, 1, size=2)
        V = lyapunov_function(x)
        f = nonlinear_system(x)
        V_next = lyapunov_function(x + 0.01 * f)

        if V_next - V > 1e-6:
            return False

    return True

if __name__ == "__main__":
    if not lasalle_check():
        raise RuntimeError("LaSalle gate failed.")
    print("Nonlinear LaSalle gate passed.")
