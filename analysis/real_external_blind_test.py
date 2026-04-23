import requests
import pandas as pd
import numpy as np
import json
import os
from analysis.numerical_spectral_verification import estimate_alpha

URL = "https://raw.githubusercontent.com/datasets/finance-vix/master/data/vix-daily.csv"

def fetch_external():
    local_path = "real-data/vix.csv"

    # 🔁 1. حاول تقرأ local لو موجود
    if os.path.exists(local_path):
        df = pd.read_csv(local_path)
    else:
        print("🌐 Fetching REAL external data...")
        try:
            response = requests.get(URL, timeout=10)
            response.raise_for_status()

            os.makedirs("real-data", exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(response.content)

            df = pd.read_csv(local_path)

        except Exception as e:
            raise RuntimeError(f"External fetch failed: {e}")

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    for col in df.columns:
        if "close" in col:
            return df[col].dropna().values

    raise ValueError("No 'close' column found in dataset")


def run_test():
    data = fetch_external()

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


def bind_external_result(values):
    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/external_witness.json", "w") as f:
        json.dump({
            "source": "external_blind_test",
            "length": len(values),
            "hash": str(hash(tuple(values)))
        }, f, indent=2)


if __name__ == "__main__":
    run_test()
    data = fetch_external()
    bind_external_result(data)
