import json
import numpy as np
from scipy.fft import fft
from scipy.stats import normaltest

def load(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            if "MAXIMAL_FIELD:" in line:
                data.append(json.loads(line.split("MAXIMAL_FIELD:")[1].strip()))
    return data

def analyze(data):
    means = np.array([d["mean"] for d in data])
    variances = np.array([d["variance"] for d in data])

    print("Mean of Means:", np.mean(means))
    print("Std of Means:", np.std(means))

    stat, p = normaltest(means)
    print("Normality test p-value:", p)

    spectrum = np.abs(fft(means))
    dominant = np.argmax(spectrum[1:]) + 1
    print("Dominant Frequency Index:", dominant)

if __name__ == "__main__":
    data = load("field.log")
    analyze(data)
