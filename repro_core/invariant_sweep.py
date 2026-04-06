import json
import math
import random

from entropy_invariant import invariant

def sweep(seeds, N, bins=50):
    results = []
    max_I = 0

    for s in seeds:
        r = invariant(seed=s, N=N, bins=bins)
        max_I = max(max_I, r["invariant"])
        results.append({
            "seed": s,
            "variance": r["variance"],
            "entropy": r["entropy"],
            "invariant": r["invariant"]
        })

    summary = {
        "N": N,
        "bins": bins,
        "max_invariant_observed": max_I,
        "num_seeds": len(seeds)
    }

    return {
        "summary": summary,
        "results": results
    }

if __name__ == "__main__":
    seeds = range(0, 200)  # widen gradually
    output = sweep(seeds, N=50000, bins=50)
    print(json.dumps(output["summary"], indent=2))
