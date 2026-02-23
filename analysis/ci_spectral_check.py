import numpy as np
import json
from scipy.signal import find_peaks
from scipy.stats import zscore

try:
    data = np.loadtxt("analysis/latest_metrics.txt")
except:
    print("No data file found.")
    exit()

if len(data) < 128:
    print("Insufficient data.")
    exit()

fft_vals = np.fft.fft(data)
power = np.abs(fft_vals)**2

z = zscore(power)
peaks, _ = find_peaks(z, height=3)  # 3-sigma threshold

if len(peaks) > 0:
    report = {
        "dominant_indices": peaks.tolist(),
        "max_zscore": float(np.max(z)),
        "sample_size": len(data)
    }

    with open("analysis/significant_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Significant periodicity detected.")
else:
    print("No statistically significant periodicity.")
