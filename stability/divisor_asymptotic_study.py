import os
import json
import math
import numpy as np
import statistics

def divisor_count(n):
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1 if i * i == n else 2
        i += 1
    return count

def theoretical_upper_bound(k):
    if k < 3:
        return 10  # trivial safe bound for small k
    return math.exp(2 * math.log(k) / math.log(math.log(k)))

def run(limit=50000):
    ratios = []
    max_ratio = 0
    max_k = 1

    for k in range(3, limit + 1):
        d = divisor_count(k)
        logk = math.log(k)

        ratio = d / logk
        ratios.append(ratio)

        if ratio > max_ratio:
            max_ratio = ratio
            max_k = k

        # Correct asymptotic guard
        if d > theoretical_upper_bound(k):
            raise ValueError(f"Asymptotic bound violation at k={k}")

    result = {
        "limit": limit,
        "mean_ratio": statistics.mean(ratios),
        "median_ratio": statistics.median(ratios),
        "max_ratio": max_ratio,
        "max_k": max_k
    }

    N = int(os.getenv("ASYMPTOTIC_N", "5000"))

    n_values = []
    ratios = []
    
    for n in range(2, N + 1):
        # احسب tau(n) أو ratio الفعلي عند
        tau = sum(1 for k in range(1, int(np.sqrt(n)) + 1) if n % k == 0) * 2
        bound = 2 * np.sqrt(n)
        ratio = tau / bound
        
        n_values.append(n)
        ratios.append(ratio)
        
        report = {
            "n_values": n_values,
            "ratios": ratios
        }
        
        print(json.dumps(report))

if __name__ == "__main__":
    run()
