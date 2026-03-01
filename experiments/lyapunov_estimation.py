# experiments/lyapunov_estimation.py

import numpy as np
import os

np.seterr(all="ignore")

def logistic_map(x, r=4.0):
    return r * x * (1 - x)

def estimate_lyapunov(x0, n=1000, eps=1e-8):
    try:
        x = x0
        x_perturbed = x0 + eps
        lyap_sum = 0.0

        for _ in range(n):
            x = logistic_map(x)
            x_perturbed = logistic_map(x_perturbed)

            diff = abs(x_perturbed - x)
            if diff == 0 or np.isnan(diff) or np.isinf(diff):
                return None

            lyap_sum += np.log(abs(diff / eps))
            x_perturbed = x + eps

        return lyap_sum / n

    except Exception:
        return None


def safe_mean(arr):
    clean = [x for x in arr if x is not None and not np.isnan(x) and not np.isinf(x)]
    if len(clean) == 0:
        return float("nan")
    return float(np.mean(clean))


def failure_ratio(arr):
    total = len(arr)
    failed = len([x for x in arr if x is None or np.isnan(x) or np.isinf(x)])
    return failed / total if total > 0 else float("nan")


if __name__ == "__main__":
    seeds = range(500)
    exponents = []

    for s in seeds:
        np.random.seed(s)
        x0 = np.random.rand()
        lyap = estimate_lyapunov(x0)
        exponents.append(lyap)

    mean_lyap = safe_mean(exponents)
    fail_rate = failure_ratio(exponents)

    os.makedirs("../data", exist_ok=True)

    with open("../data/lyapunov.txt", "w") as f:
        f.write(f"mean_lyapunov: {mean_lyap}\n")
        f.write(f"failure_ratio: {fail_rate}\n")

    print("Lyapunov estimation complete")
