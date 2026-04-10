import os
import numpy as np
import pandas as pd

def ensure_market_proxy():
    path = "real-data/market_proxy.csv"

    if os.path.exists(path):
        print("market_proxy.csv exists.")
        return

    print("Creating fallback market proxy dataset...")

    os.makedirs("real-data", exist_ok=True)

    t = np.arange(0, 2000)

    # simulate market-like noisy signal
    trend = 0.001 * t
    seasonal = 0.05 * np.sin(2 * np.pi * t / 50)
    noise = np.random.normal(0, 0.02, len(t))

    price = 100 + trend + seasonal + noise

    df = pd.DataFrame({
        "t": t,
        "value": price
    })

    df.to_csv(path, index=False)

    print("market_proxy.csv created.")

def run():
    ensure_market_proxy()

if __name__ == "__main__":
    run()
