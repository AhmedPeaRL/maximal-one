import os
import json
import math
import statistics
import numpy as np


def divisor_count(n):
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1 if i * i == n else 2
        i += 1
    return count


def run():

    N = int(os.getenv("ASYMPTOTIC_N", "5000"))

    n_values = []
    ratios = []

    max_ratio = 0.0
    max_n = 1

    running_supremum = []

    for n in range(2, N + 1):

        tau = divisor_count(n)
        bound = 2 * math.sqrt(n)

        ratio = tau / bound

        n_values.append(n)
        ratios.append(ratio)

        if ratio > max_ratio:
            max_ratio = ratio
            max_n = n

        running_supremum.append(max_ratio)

    last_window = ratios[-100:] if len(ratios) >= 100 else ratios

    report = {
        "N": N,
        "max_ratio": max_ratio,
        "argmax_n": max_n,
        "final_ratio": ratios[-1],
        "mean_last_window": statistics.mean(last_window),
        "global_mean_ratio": statistics.mean(ratios),
        "global_median_ratio": statistics.median(ratios),
        "n_values": n_values,
        "ratios": ratios,
        "running_supremum": running_supremum
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
