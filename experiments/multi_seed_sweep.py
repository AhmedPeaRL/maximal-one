import numpy as np
import pandas as pd
from scipy.signal import welch

def spectral_exponent(signal):
    freqs, psd = welch(signal, nperseg=256)
    freqs = freqs[1:]
    psd = psd[1:]
    log_f = np.log(freqs)
    log_p = np.log(psd)
    slope, _ = np.polyfit(log_f, log_p, 1)
    return -slope

def generate_signal(seed, n=2048):
    np.random.seed(seed)
    return np.cumsum(np.random.normal(size=n))

def main():
    results = []

    for seed in range(5000):
        signal = generate_signal(seed)
        value = np.mean(signal)
        alpha = spectral_exponent(signal)

        results.append({
            "seed": seed,
            "value": value,
            "spectral_exponent": alpha
        })

        print(f"Seed {seed} done")

    df = pd.DataFrame(results)
    df.to_csv("../data/multi_seed_results.csv", index=False)
    print("Saved: ../data/multi_seed_results.csv")

if __name__ == "__main__":
    main()
