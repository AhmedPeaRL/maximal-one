import os
import pandas as pd
from analysis.numerical_spectral_verification import estimate_alpha

DATA_DIR = "real-data"

def load_series(path):
    df = pd.read_csv(path)

    df = df.dropna(axis=1, how="all")  # remove empty columns

    for col in df.columns:
        if df[col].dtype != "object":
            return df[col].values

    raise ValueError(f"No valid numeric column in {path}")

def main():
    results = []
    failed_count = 0
    total_count = 0

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            total_count += 1
            path = os.path.join(DATA_DIR, file)
            try:
                series = load_series(path)

                if len(series) < 10:
                    raise ValueError("Series too small")

                alpha = estimate_alpha(series)
                results.append((file, alpha))
                print(f"{file}: alpha={alpha}")

            except Exception as e:
                failed_count += 1
                print(f"{file}: FAILED ({e})")

    if len(results) < 2:
        raise SystemExit("❌ Not enough valid datasets")

    failure_ratio = failed_count / total_count

    print(f"\nSummary:")
    print(f"Total datasets: {total_count}")
    print(f"Failures: {failed_count}")
    print(f"Failure ratio: {failure_ratio:.2f}")

    if failure_ratio > 0.2:
        raise SystemExit("❌ Too many dataset failures — invariant not stable")

    print("✅ CROSS DOMAIN VALIDATION DONE")

if __name__ == "__main__":
    main()
