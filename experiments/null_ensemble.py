import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

def generate_random_walk(n):
    steps = np.random.normal(0, 1, n)
    return np.cumsum(steps)

def spectral_exponent(signal):
    fft = np.fft.fft(signal)
    power = np.abs(fft)**2
    freqs = np.fft.fftfreq(len(signal))
    mask = freqs > 0
    freqs = freqs[mask]
    power = power[mask]
    coeffs = np.polyfit(np.log(freqs), np.log(power), 1)
    return -coeffs[0]

def main():
    real = pd.read_csv("../data/multi_seed_results.csv")["spectral_exponent"].values

    null_vals = []
    for i in range(5000):
        rw = generate_random_walk(len(real))
        null_vals.append(spectral_exponent(rw))

    null_vals = np.array(null_vals)

    tstat, pval = ttest_ind(real, null_vals, equal_var=False)

    print("=== Null Ensemble Comparison ===")
    print("Real mean:", np.mean(real))
    print("Null mean:", np.mean(null_vals))
    print("t-stat:", tstat)
    print("p-value:", pval)

if __name__ == "__main__":
    main()
