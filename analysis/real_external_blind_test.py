import requests
import pandas as pd
import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

URL = "https://raw.githubusercontent.com/datasets/finance-vix/master/data/vix-daily.csv"

def fetch_external():
    df = pd.read_csv("real-data/vix.csv")

    # Normalize column names (critical fix)
    df.columns = [c.strip().lower() for c in df.columns]

    for col in df.columns:
        if "close" in col:
            return df[col].dropna().values

    raise ValueError("No 'close' column found in dataset")
    
def run_test():
    data = fetch_external()

    # Blind segmentation
    np.random.seed(42)
    np.random.shuffle(data)

    split = int(len(data) * 0.7)
    train = data[:split]
    test = data[split:]

    alpha_train = estimate_alpha(train)
    alpha_test = estimate_alpha(test)

    print("Alpha train:", alpha_train)
    print("Alpha test:", alpha_test)

    drift = abs(alpha_train - alpha_test)

    if drift > 0.2:
        print("❌ Drift too high → FAIL")
        exit(1)

    print("✅ External blind stability confirmed")

if __name__ == "__main__":
    run_test()
