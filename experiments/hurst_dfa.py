import numpy as np
import pandas as pd

def dfa(signal, min_lag=4, max_lag=50):
    n = len(signal)
    lags = np.arange(min_lag, max_lag)

    tau = []
    for lag in lags:
        if lag >= n:
            continue
        segments = n // lag
        if segments < 2:
            continue

        reshaped = signal[:segments*lag].reshape((segments, lag))
        rms = np.sqrt(np.mean(np.var(reshaped, axis=1)))
        if rms > 0:
            tau.append(rms)
        else:
            tau.append(np.nan)

    tau = np.array(tau)
    valid = (~np.isnan(tau)) & (tau > 0)

    if np.sum(valid) < 2:
        return np.nan

    poly = np.polyfit(np.log(lags[valid]), np.log(tau[valid]), 1)
    return poly[0]

def main():
    df = pd.read_csv("../data/multi_seed_results.csv")
    values = df["spectral_exponent"].values

    h = dfa(values)

    print("=== Hurst via DFA ===")
    print("Hurst estimate:", h)

if __name__ == "__main__":
    main()
