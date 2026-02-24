import json
import numpy as np
from maximal_one.master_experiment import run_experiment
import sys
import os

BASELINE_PATH = "baseline_distribution.json"

def compute_distribution(n=100):
    results = []
    for seed in range(n):
        r = run_experiment(seed=seed)
        results.append(r["max_zscore"])
    return np.array(results)

def create_baseline(dist):
    return {
        "mean": float(np.mean(dist)),
        "std": float(np.std(dist)),
        "p99": float(np.percentile(dist, 99))
    }

def load_or_create_baseline():
    if os.path.exists(BASELINE_PATH):
        with open(BASELINE_PATH) as f:
            return json.load(f)

    print("Creating new SPC baseline...")
    dist = compute_distribution(200)
    baseline = create_baseline(dist)

    with open(BASELINE_PATH, "w") as f:
        json.dump(baseline, f, indent=2)

    return baseline

def main():
    baseline = load_or_create_baseline()

    dist = compute_distribution(100)

    mean = float(np.mean(dist))
    std = float(np.std(dist))
    p99 = float(np.percentile(dist, 99))

    violation = False

    if p99 > baseline["p99"] * 1.15:
        print("CONTROL VIOLATION: Tail expansion detected")
        violation = True

    if abs(mean - baseline["mean"]) > 3 * baseline["std"]:
        print("CONTROL VIOLATION: Mean drift detected")
        violation = True

    if violation:
        sys.exit(1)

    print("SPC Stable.")
    sys.exit(0)

if __name__ == "__main__":
    main()
