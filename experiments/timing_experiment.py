import time
import json
import platform
import socket
import numpy as np
from scipy.fft import rfft, rfftfreq

SAMPLES = 1_000_000
OUTPUT_FILE = "timing_results.json"


def collect_deltas(n):
    deltas = np.empty(n, dtype=np.float64)
    last = time.perf_counter_ns()
    for i in range(n):
        current = time.perf_counter_ns()
        deltas[i] = current - last
        last = current
    return deltas


def compute_spectrum(deltas):
    deltas = deltas - np.mean(deltas)
    fft_vals = np.abs(rfft(deltas))
    freqs = rfftfreq(len(deltas), d=1)
    return freqs, fft_vals


def monte_carlo_baseline(n, simulations=100):
    max_vals = []
    for _ in range(simulations):
        noise = np.random.normal(0, 1, n)
        fft_vals = np.abs(rfft(noise))
        max_vals.append(np.max(fft_vals))
    return np.mean(max_vals), np.std(max_vals)


def environment_metadata():
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "hostname": socket.gethostname(),
    }


def main():
    deltas = collect_deltas(SAMPLES)
    freqs, spectrum = compute_spectrum(deltas)

    max_observed = float(np.max(spectrum))
    baseline_mean, baseline_std = monte_carlo_baseline(len(deltas))

    z_score = (max_observed - baseline_mean) / baseline_std

    result = {
        "environment": environment_metadata(),
        "max_spectrum": max_observed,
        "baseline_mean": baseline_mean,
        "baseline_std": baseline_std,
        "z_score": z_score,
        "significant": bool(z_score > 10),
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=4)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
