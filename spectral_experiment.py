import numpy as np
from scipy.signal import find_peaks
from scipy.stats import zscore

def run_spectral_test(data):

    fft_vals = np.fft.fft(data)
    power = np.abs(fft_vals)**2

    z = zscore(power)

    peaks, properties = find_peaks(z, height=3)

    significant = len(peaks) > 0

    return {
        "max_zscore": float(np.max(z)),
        "significant": significant,
        "peak_indices": peaks.tolist()
    }
