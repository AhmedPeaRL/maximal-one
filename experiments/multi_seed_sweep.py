import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import linregress
import os

OUTPUT_PATH = "../data/multi_seed_results.csv"
N = 4096
SEEDS = range(0, 50)  # 50 independent seeds
BOOTSTRAP_ITER = 1000

def generate_process(seed):
    np.random.seed(seed)
    return np.cumsum(np.random.randn(N))  # integrated white noise

def estimate_alpha(x):
    f, Pxx = welch(x, nperseg=256)
    log_f = np.log(f[1:])
    log_P = np.log(Pxx[1:])
    slope, _, _, _, _ = linregress(log_f, log_P)
    return -slope

def bootstrap_alpha(x):
    alphas = []
    for _ in range(BOOTSTRAP_ITER):
        resample = np.random.choice(x, size=len(x), replace=True)
        alphas.append(estimate_alpha(resample))
    return np.mean(alphas), np.std(alphas)

def main():
    results = []
    for seed in SEEDS:
        x = generate_process(seed)
        alpha = estimate_alpha(x)
        mu_boot, std_boot = bootstrap_alpha(x)
        results.append({
            "seed": seed,
            "alpha": alpha,
            "mu_boot": mu_boot,
            "std_boot": std_boot
        })
        print(f"Seed {seed} done")

    df = pd.DataFrame(results)
    os.makedirs("../data", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print("Saved:", OUTPUT_PATH)

if __name__ == "__main__":
    main()
