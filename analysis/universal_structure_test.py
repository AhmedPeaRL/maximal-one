import numpy as np
from itertools import combinations

def relative_structure(values):
    values = np.array(values)

    # normalize
    norm = (values - np.mean(values)) / (np.std(values) + 1e-9)

    return norm

def pairwise_distances(v):
    return [abs(a - b) for a, b in combinations(v, 2)]

def run_test(results):
    raw = np.array(list(results.values()))

    norm = relative_structure(raw)
    dists = pairwise_distances(norm)

    spread = max(dists)

    print("Normalized structure:", norm)
    print("Pairwise spread:", spread)

    if spread > 1.5:
        print("❌ Structure not preserved")
        exit(1)

    print("✅ Universal structure detected")
