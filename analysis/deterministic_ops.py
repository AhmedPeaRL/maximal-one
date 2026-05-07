import os
import random
import numpy as np

def deterministic_seed(seed=42):
    """
    Enforce deterministic numerical behavior
    across numpy / random / hash layers.
    """

    os.environ["PYTHONHASHSEED"] = str(seed)

    random.seed(seed)

    np.random.seed(seed)

def stable_log(x):
    return np.log(np.round(x, 12) + 1e-12)

def stable_fft_power(series):
    fft_vals = np.fft.rfft(series)
    psd = (np.abs(fft_vals) ** 2) / len(series)
    return np.round(psd, 10)

def stable_smoothing(x):
    """
    Deterministic smoothing
    replacing scipy-dependent filters.
    """
    kernel = np.ones(2) / 2.0
    return np.convolve(x, kernel, mode="same")

def stable_polyfit(x, y):
    """
    Stable least-squares linear fit.
    """
    A = np.vstack([x, np.ones(len(x))]).T

    coeffs = np.linalg.lstsq(
        A,
        y,
        rcond=None
    )[0]

    return float(np.round(coeffs[0], 10))
