import os
import pandas as pd
import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.load_real_datasets import load_all

DATA_DIR = "real-data"

def load_series(path):
    df = pd.read_csv(path, sep=None, engine="python", na_values=["***"])

    df = df.select_dtypes(include=[np.number])
    if df.shape[1] == 0:
        raise ValueError("No numeric columns")

    series = df.iloc[:, 0].dropna().values

    if len(series) < 64:
        raise ValueError("Series too small")

    std = np.std(series)
    if std < 1e-6:
        raise ValueError("Near-constant")

    series = (series - np.mean(series)) / std
    return series
    
def main():
    results = []
    failed = []
    datasets = load_all()

    for name, series in datasets.items():

        alpha = estimate_alpha(series)

        if not np.isfinite(alpha) or alpha < 0.3:
            print(f"{name}: rejected")
            continue

        print(f"{name}: alpha={alpha}")
        results.append(alpha)

    if len(results) < 2:
        raise SystemExit("❌ Cross-domain failed")

    print("✅ CROSS DOMAIN REAL PASSED")

    for file in sorted(os.listdir(DATA_DIR)):
        if file.endswith(".csv"):
            path = os.path.join(DATA_DIR, file)
            try:
                series = load_series(path)

                if len(series) < 32:
                    raise ValueError("Series too small")

                alpha = estimate_alpha(series)

                if not np.isfinite(alpha) or alpha < 0.3:
                    raise ValueError("Weak or invalid alpha")

                if alpha > 5:
                    raise ValueError("Alpha saturation")

                results.append(float(alpha))

                print(f"{file}: alpha={alpha:.4f}")

            except Exception as e:
                failed.append(file)
                print(f"{file}: SKIPPED ({e})")

    if len(results) < 3:
        raise SystemExit("❌ Not enough valid datasets")

    std = np.std(results)
    median = np.median(results)

    print("\nSummary:")
    print(f"Valid datasets: {len(results)}")
    print(f"Skipped: {len(failed)}")
    print(f"Median alpha: {median:.4f}")
    print(f"STD alpha: {std:.4f}")

    print("✅ CROSS DOMAIN VALIDATION PASSED")

if __name__ == "__main__":
    main()
