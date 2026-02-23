import numpy as np
import time
import platform
import os
from scipy.signal import get_window

# =============================
# CONFIG
# =============================

SAMPLE_SIZE = int(os.getenv("SAMPLE_SIZE", "1000000"))
WINDOW_TYPE = os.getenv("WINDOW_TYPE", "none")
NORMALIZATION = os.getenv("NORMALIZATION", "raw")

# =============================
# TIMER SAMPLING
# =============================

def collect_deltas(n):
    times = np.empty(n)
    for i in range(n):
        times[i] = time.perf_counter_ns()
    deltas = np.diff(times)
    return deltas.astype(np.float64)

# =============================
# NORMALIZATION
# =============================

def normalize(data):
    if NORMALIZATION == "variance_normalized":
        return (data - np.mean(data)) / np.std(data)
    elif NORMALIZATION == "power_normalized":
        return data / np.sqrt(np.sum(data**2))
    return data

# =============================
# WINDOW
# =============================

def apply_window(data):
    if WINDOW_TYPE == "none":
        return data
    window = get_window(WINDOW_TYPE, len(data))
    return data * window

# =============================
# FFT ANALYSIS
# =============================

def compute_spectrum(data):
    spectrum = np.abs(np.fft.rfft(data))
    return spectrum

# =============================
# MONTE CARLO BASELINE
# =============================

def monte_carlo(n, trials=50):
    peaks = []
    for _ in range(trials):
        noise = np.random.normal(0, 1, n)
        noise = normalize(noise)
        noise = apply_window(noise)
        spec = compute_spectrum(noise)
        peaks.append(np.max(spec))
    return np.mean(peaks), np.std(peaks)

# =============================
# MAIN
# =============================

if __name__ == "__main__":

    deltas = collect_deltas(SAMPLE_SIZE)
    deltas = normalize(deltas)
    deltas = apply_window(deltas)

    spectrum = compute_spectrum(deltas)
    observed_max = np.max(spectrum)

    baseline_mean, baseline_std = monte_carlo(len(deltas))

    z_score = (observed_max - baseline_mean) / baseline_std

    print("\n=== SYSTEM INFO ===")
    print("OS:", platform.system())
    print("Arch:", platform.machine())
    print("CPU:", platform.processor())
    print("Sample size:", SAMPLE_SIZE)
    print("Window:", WINDOW_TYPE)
    print("Normalization:", NORMALIZATION)

    print("\n=== RESULTS ===")
    print("Observed Max:", observed_max)
    print("Baseline Mean:", baseline_mean)
    print("Baseline Std:", baseline_std)
    print("Z-score:", z_score)
    print("Significant:", z_score > 10)
