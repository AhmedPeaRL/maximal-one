import numpy as np
from spectral_experiment import run_spectral_test
from theoretical_guard import validate_environment
import json
import time

def main():

    validate_environment()

    np.random.seed(42)
    baseline = np.random.normal(0, 1, 2048)

    result = run_spectral_test(baseline, alpha=0.01)

    report = {
        "timestamp": time.time(),
        "max_zscore": result["max_zscore"],
        "empirical_threshold": result["empirical_threshold"],
        "significant": result["significant"],
        "sample_size": len(baseline),
        "null_hypothesis": "No intrinsic periodic structure"
    }

    with open("state.json", "w") as f:
        json.dump(report, f, indent=2)

    print(report)

def run_experiment(seed=None):
    if seed is not None:
        np.random.seed(seed)

    # === Core stochastic model ===
    data = np.random.normal(loc=0.0, scale=1.0, size=1000)

    mean = float(np.mean(data))
    std = float(np.std(data))
    z_score = float(mean / (std / np.sqrt(len(data))))

    result = {
        "mean": mean,
        "std": std,
        "max_zscore": abs(z_score),
        "significant": abs(z_score) > 3.0
    }

    return result


if __name__ == "__main__":
    result = run_experiment(seed=42)

    with open("state.json", "w") as f:
        json.dump(result, f, indent=2)

    if result["significant"]:
        print("Significant deviation detected.")
        exit(1)
    else:
        print("Null hypothesis holds.")

if __name__ == "__main__":
    main()
