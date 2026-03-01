import numpy as np
import pandas as pd


def dfa(signal, min_lag=4, max_lag=50):
    n = len(signal)

    lags = []
    tau = []

    for lag in range(min_lag, max_lag):
        if lag >= n:
            continue

        segments = n // lag
        if segments < 2:
            continue

        reshaped = signal[:segments * lag].reshape((segments, lag))
        rms = np.sqrt(np.mean(np.var(reshaped, axis=1)))

        if rms > 0 and np.isfinite(rms):
            lags.append(lag)
            tau.append(rms)

    lags = np.array(lags)
    tau = np.array(tau)

    if len(lags) < 2:
        return np.nan

    log_lags = np.log(lags)
    log_tau = np.log(tau)

    coeffs = np.polyfit(log_lags, log_tau, 1)

    return coeffs[0]


def main():
    df = pd.read_csv("../data/multi_seed_results.csv")

    if "spectral_exponent" not in df.columns:
        raise ValueError("spectral_exponent column missing")

    values = df["spectral_exponent"].values

    h = dfa(values)

    print("=== Hurst via DFA ===")
    print("Hurst estimate:", h)


if __name__ == "__main__":
    main()
