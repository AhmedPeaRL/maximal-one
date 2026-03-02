# analysis/lyapunov_strict_scan.py

import numpy as np

def logistic_map(r, x):
    return r * x * (1 - x)

def estimate_lyapunov(r, n=10000):
    x = 0.5
    lyap = 0
    for _ in range(n):
        x = logistic_map(r, x)
        lyap += np.log(abs(r * (1 - 2 * x)))
    return lyap / n

if __name__ == "__main__":
    rs = np.linspace(2.5, 4.0, 200)
    results = []

    for r in rs:
        results.append((r, estimate_lyapunov(r)))

    positive = sum(1 for _, l in results if l > 0)

    print("Positive Lyapunov regions:", positive)
