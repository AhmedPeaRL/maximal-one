# analysis/nonlinear_real_world_scan.py

import numpy as np
from real_data_adapter import load_csv_series, normalize
from numpy.fft import fft

def spectral_profile(series):
    freq = np.abs(fft(series))
    power = np.log(freq + 1e-12)
    return np.mean(power), np.std(power)

def lyapunov_estimate(series):
    diffs = np.diff(series)
    return np.mean(np.log(np.abs(diffs) + 1e-12))

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python nonlinear_real_world_scan.py data.csv")
        exit(1)

    data = normalize(load_csv_series(sys.argv[1]))

    mean_power, std_power = spectral_profile(data)
    lyap = lyapunov_estimate(data)

    print("Spectral mean:", mean_power)
    print("Spectral std:", std_power)
    print("Lyapunov proxy:", lyap)
