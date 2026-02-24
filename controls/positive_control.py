import numpy as np


def inject_shift(sample, amplitude):
    return sample + amplitude


def detect_shift(sample, baseline_mean, baseline_std, alpha=0.01):
    z = abs(np.mean(sample) - baseline_mean) / baseline_std
    threshold = 2.58  # approx for alpha=0.01
    return z > threshold, z
