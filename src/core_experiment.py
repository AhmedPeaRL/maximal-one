import numpy as np
from scipy.signal import periodogram
from scipy.stats import norm
from .statistics_utils import compute_zscores

def run_periodicity_test(signal, fs=1.0):
    freqs, power = periodogram(signal, fs=fs)

    zscores = compute_zscores(power)
    max_z = np.max(zscores)

    # Convert z-score to p-value (one-sided)
    p_values = 1 - norm.cdf(zscores)

    return {
        "freqs": freqs,
        "power": power,
        "zscores": zscores,
        "max_zscore": float(max_z),
        "p_values": p_values
    }
