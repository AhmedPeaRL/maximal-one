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

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run()
