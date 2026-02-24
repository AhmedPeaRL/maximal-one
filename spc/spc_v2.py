import numpy as np
from scipy.stats import norm

def compute_z(value, mean, std):
    if std == 0:
        return 0.0
    return (value - mean) / std

def spc_check(sample, baseline, alpha=0.01):
    """
    Distribution-aware SPC check.
    Baseline must include:
        mean_mean
        mean_std
        std_mean
        std_std
    """

    sample_mean = np.mean(sample)
    sample_std = np.std(sample)

    # Z-scores against baseline distribution
    mean_z = compute_z(
        sample_mean,
        baseline["mean_mean"],
        baseline["mean_std"]
    )

    std_z = compute_z(
        sample_std,
        baseline["std_mean"],
        baseline["std_std"]
    )

    # two-sided threshold
    threshold = norm.ppf(1 - alpha/2)

    mean_fail = abs(mean_z) > threshold
    std_fail = abs(std_z) > threshold

    return {
        "sample_mean": float(sample_mean),
        "sample_std": float(sample_std),
        "mean_z": float(mean_z),
        "std_z": float(std_z),
        "threshold": float(threshold),
        "mean_fail": bool(mean_fail),
        "std_fail": bool(std_fail),
    }
