# System Pattern Observatory - Analysis Engine

import json
import numpy as np
import matplotlib.pyplot as plt

def load_metrics(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            if "SPO_METRIC:" in line:
                json_part = line.split("SPO_METRIC:")[1].strip()
                data.append(json.loads(json_part))
    return data

def analyze(metrics):
    durations = np.array([m["loadDurationMs"] for m in metrics])
    entropy_vals = np.array([m["domEntropy"] for m in metrics])

    print("Mean Load Time:", np.mean(durations))
    print("Std Dev Load Time:", np.std(durations))
    print("Mean Entropy:", np.mean(entropy_vals))

    plt.figure()
    plt.plot(durations)
    plt.title("Load Duration Over Time")
    plt.show()

    plt.figure()
    plt.plot(entropy_vals)
    plt.title("DOM Entropy Over Time")
    plt.show()

if __name__ == "__main__":
    metrics = load_metrics("metrics.log")
    analyze(metrics)
