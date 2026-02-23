import numpy as np
from spectral_experiment import run_spectral_test
from theoretical_guard import validate_environment
import json
import time

def main():

    validate_environment()

    print("Collecting synthetic control data...")

    # Synthetic baseline
    np.random.seed(42)
    baseline = np.random.normal(0, 1, 2048)

    result = run_spectral_test(baseline)

    report = {
        "timestamp": time.time(),
        "max_zscore": result["max_zscore"],
        "significant": result["significant"],
        "sample_size": len(baseline),
        "null_hypothesis": "No intrinsic periodic structure"
    }

    with open("state.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Experiment complete.")
    print(report)

if __name__ == "__main__":
    main()
