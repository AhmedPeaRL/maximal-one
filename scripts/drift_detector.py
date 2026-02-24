import json
import numpy as np
from scipy.stats import ks_2samp

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def compute_drift(current_data, baseline_metrics):
    mean_diff = abs(np.mean(current_data) - baseline_metrics["mean"])
    std_diff = abs(np.std(current_data) - baseline_metrics["std"])
    p99 = np.percentile(current_data, 99)

    ks_stat, ks_p = ks_2samp(
        current_data,
        np.random.normal(
            baseline_metrics["mean"],
            baseline_metrics["std"],
            len(current_data)
        )
    )

    return {
        "mean_diff": float(mean_diff),
        "std_diff": float(std_diff),
        "p99": float(p99),
        "ks_stat": float(ks_stat),
        "ks_pvalue": float(ks_p)
    }

if __name__ == "__main__":
    baseline = load_json("baselines/baseline_v1.json")
    data = np.load("current_sample.npy")
    result = compute_drift(data, baseline["metrics"])
    print(json.dumps(result, indent=2))
