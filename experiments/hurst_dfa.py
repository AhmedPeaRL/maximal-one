import numpy as np
import pandas as pd

def hurst_exponent(ts):
    lags = range(2, 100)
    tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0]

def main():
    df = pd.read_csv("../data/multi_seed_results.csv")
    x = df["value"].values
    H = hurst_exponent(x)
    print("Hurst exponent:", H)

if __name__ == "__main__":
    main()
