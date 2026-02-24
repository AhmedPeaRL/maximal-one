import numpy as np
import json
from master_experiment import run_experiment


def compute_baseline_distribution(seeds=200):
    results = []
    for seed in range(seeds):
        r = run_experiment(seed=seed)
        results.append(r["max_zscore"])
    return np.array(results)


def detect_drift(current_value, baseline):
    mean = np.mean(baseline)
    std = np.std(baseline)
    z = (current_value - mean) / std
    return abs(z) > 4.0


if __name__ == "__main__":
    baseline = compute_baseline_distribution()
    current = run_experiment(seed=999)["max_zscore"]

    drift = detect_drift(current, baseline)

    report = {
        "baseline_mean": float(np.mean(baseline)),
        "baseline_std": float(np.std(baseline)),
        "current": float(current),
        "drift_detected": drift
    }

    with open("drift_report.json", "w") as f:
        json.dump(report, f, indent=2)

    if drift:
        raise SystemExit("Drift detected.")
