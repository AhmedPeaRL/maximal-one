import numpy as np


def spc_check(sample, baseline, tests=2, alpha=0.01):
    mean = np.mean(sample)
    std = np.std(sample)

    corrected_alpha = alpha / tests
    threshold = 2.58  # approximate z for 0.01

    mean_z = abs(mean - baseline["mean"]) / baseline["std"]
    std_z = abs(std - baseline["std"]) / baseline["std"]

    mean_fail = mean_z > threshold
    std_fail = std_z > threshold

    return {
        "mean_z": float(mean_z),
        "std_z": float(std_z),
        "mean_fail": mean_fail,
        "std_fail": std_fail,
        "corrected_alpha": corrected_alpha,
    }
