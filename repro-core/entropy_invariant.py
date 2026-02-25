import random
import math
import hashlib
import json

def deterministic_sequence(seed, N):
    random.seed(seed)
    return [random.random() for _ in range(N)]

def empirical_variance(data):
    mean = sum(data) / len(data)
    return sum((x - mean) ** 2 for x in data) / len(data)

def entropy(data, bins=50):
    counts = [0]*bins
    for x in data:
        idx = min(int(x * bins), bins - 1)
        counts[idx] += 1

    N = len(data)
    H = 0
    for c in counts:
        if c > 0:
            p = c / N
            H -= p * math.log(p)
    return H

def invariant(seed, N, bins=50):
    data = deterministic_sequence(seed, N)
    var = empirical_variance(data)
    H = entropy(data, bins)
    theoretical_var = 1/12
    max_entropy = math.log(bins)

    I = abs(var - theoretical_var) * abs(H - max_entropy)

    return {
        "variance": var,
        "entropy": H,
        "invariant": I
    }

if __name__ == "__main__":
    result = invariant(seed=42, N=100000)
    print(json.dumps(result, indent=2))
