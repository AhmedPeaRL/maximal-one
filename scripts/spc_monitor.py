import json
import numpy as np

CONTROL_LIMITS = {
    "mean_ucl": 0.05,
    "std_ucl": 0.05,
    "p99_ucl": 4.0
}

def evaluate(metrics):
    violations = []

    if metrics["mean_diff"] > CONTROL_LIMITS["mean_ucl"]:
        violations.append("Mean out of control")

    if metrics["std_diff"] > CONTROL_LIMITS["std_ucl"]:
        violations.append("Std deviation out of control")

    if metrics["p99"] > CONTROL_LIMITS["p99_ucl"]:
        violations.append("Tail explosion detected")

    return violations

if __name__ == "__main__":
    with open("drift_output.json") as f:
        metrics = json.load(f)

    violations = evaluate(metrics)

    if violations:
        print("CONTROL VIOLATION:")
        for v in violations:
            print(v)
        exit(1)
    else:
        print("Process within statistical control.")
