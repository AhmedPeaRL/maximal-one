import math
import json
import statistics

def divisor_count(n):
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1 if i * i == n else 2
        i += 1
    return count

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

    result = {
        "limit": limit,
        "mean_ratio": statistics.mean(ratios),
        "median_ratio": statistics.median(ratios),
        "max_ratio": max_ratio,
        "max_k": max_k
    }

    print(json.dumps(result, indent=2))

    # Stability guard: d(k) must stay below k^(0.2) for tested range
    for k in range(3, limit + 1):
        if divisor_count(k) > k ** 0.2:
            raise ValueError(f"Unexpected growth anomaly at k={k}")

if __name__ == "__main__":
    run()
