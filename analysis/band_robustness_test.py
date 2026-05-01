import numpy as np
import pandas as pd
from analysis.numerical_spectral_verification import estimate_alpha

def test_bands(series):

    bands = [
        (0.01, 0.1),
        (0.02, 0.25),
        (0.05, 0.3),
        (0.01, 0.4)
    ]

    results = []

    for low, high in bands:
        alpha = estimate_alpha(series)
        results.append((low, high, alpha))

    return results


if __name__ == "__main__":

    df = pd.read_csv("real-data/sunspots_global.csv")

    col = "Sunspots" if "Sunspots" in df.columns else "value"

    series = df[col].values.astype(float)

    res = test_bands(series)

    for r in res:
        print(f"band {r[0]}-{r[1]} -> alpha = {r[2]}")

    print("✅ BAND ROBUSTNESS TEST DONE")
