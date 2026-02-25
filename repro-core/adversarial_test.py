import json
import subprocess
import sys
from entropy_invariant import invariant

THEORETICAL_VARIANCE = 1.0 / 12.0
TOLERANCE = 0.005  # allowed deviation


def run_kernel(seed, n):
    code = f"""
import random, json
rng = random.Random({seed})
data = [rng.random() for _ in range({n})]
mean = sum(data)/{n}
variance = sum((x-mean)**2 for x in data)/{n}
print(json.dumps({{"variance": variance}}))
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)["variance"]


def test_variance_stability():
    seeds = [1, 42, 99, 1234]
    n = 10000  # larger N for convergence

    for seed in seeds:
        variance = run_kernel(seed, n)
        if abs(variance - THEORETICAL_VARIANCE) > TOLERANCE:
            print("FAILURE_MODE: OUT_OF_STATISTICAL_BOUND")
            sys.exit(1)

    print("SURVIVED_ADVERSARIAL_STRESS")

def stress_invariant():
    worst = 0
    for seed in range(0, 500):
        r = invariant(seed=seed, N=20000)
        worst = max(worst, r["invariant"])
        if r["invariant"] > 0.01:
            print("INVARIANT_BOUND_BROKEN")
            return False
    print("INVARIANT_BOUND_HELD")
    print("max observed:", worst)
    return True

if __name__ == "__main__":
    test_variance_stability()
