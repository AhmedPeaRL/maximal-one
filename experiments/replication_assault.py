import numpy as np
from scipy.signal import welch
from scipy.stats import linregress

N = 4096
TRIALS = 100
THRESHOLD = 0.2  # aggressive deviation threshold

def generate_modified_process():
    # inject structured trend to try breaking half scaling
    x = np.cumsum(np.random.randn(N))
    trend = np.linspace(0, 50, N)
    return x + trend

def estimate_alpha(x):
    f, Pxx = welch(x, nperseg=256)
    log_f = np.log(f[1:])
    log_P = np.log(Pxx[1:])
    slope, _, _, _, _ = linregress(log_f, log_P)
    return -slope

def main():
    failures = 0
    for _ in range(TRIALS):
        x = generate_modified_process()
        alpha = estimate_alpha(x)
        if abs(alpha - 0.5) > THRESHOLD:
            failures += 1

    print("Failures:", failures, "out of", TRIALS)

if __name__ == "__main__":
    main()
