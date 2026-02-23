import time
import json
import platform
import socket
import numpy as np
from scipy.fft import rfft

SAMPLES = 1_000_000
MONTE_CARLO_RUNS = 200

def collect_deltas(n):
    deltas = np.empty(n, dtype=np.float64)
    last = time.perf_counter_ns()
    for i in range(n):
        now = time.perf_counter_ns()
        deltas[i] = now - last
        last = now
    return deltas

def spectrum(deltas):
    centered = deltas - np.mean(deltas)
    return np.abs(rfft(centered))

def monte_carlo(n, runs):
    maxima = []
    for _ in range(runs):
        noise = np.random.normal(0, 1, n)
        maxima.append(np.max(np.abs(rfft(noise))))
    return np.mean(maxima), np.std(maxima)

def environment():
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python": platform.python_version(),
        "hostname": socket.gethostname()
    }

def main():
    deltas = collect_deltas(SAMPLES)
    spec = spectrum(deltas)

    observed_max = float(np.max(spec))
    baseline_mean, baseline_std = monte_carlo(len(deltas), MONTE_CARLO_RUNS)

    z = (observed_max - baseline_mean) / baseline_std

    result = {
        "environment": environment(),
        "observed_max": observed_max,
        "baseline_mean": baseline_mean,
        "baseline_std": baseline_std,
        "z_score": z,
        "significant": bool(z > 10)
    }

    with open("timing_results.json", "w") as f:
        json.dump(result, f, indent=4)

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
