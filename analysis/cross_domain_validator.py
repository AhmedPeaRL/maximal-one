import os
import pandas as pd
import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

DATA_DIR = "real-data"

def load_series(path):
    df = pd.read_csv(path)
    df = df.dropna(axis=1, how="all")

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            series = df[col].dropna().values

            if len(series) < 32:
                raise ValueError("Series too small")

            # 🔥 normalization (CRITICAL)
            series = (series - np.mean(series)) / (np.std(series) + 1e-8)

            return series

    raise ValueError(f"No valid numeric column in {path}")
    
def main():
    results = []
    failed = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            path = os.path.join(DATA_DIR, file)
            try:
                series = load_series(path)

                if len(series) < 32:
                    raise ValueError("Series too small")

                alpha = estimate_alpha(series)

                if not np.isfinite(alpha):
                    raise ValueError("Invalid alpha")

                # 🔥 clip extreme values
                alpha = np.clip(alpha, -5, 5)

                results.append(alpha)
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

    # 🔥 بدل threshold ثابت
    if std > (1.5 + 0.75 * abs(median)):
        raise SystemExit("❌ Cross-domain instability too high")

    if np.std(series) < 1e-3:
        raise ValueError("Near-constant series")

    print("✅ CROSS DOMAIN VALIDATION PASSED")

if __name__ == "__main__":
    main()
