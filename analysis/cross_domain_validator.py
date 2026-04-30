import os
import pandas as pd
from analysis.numerical_spectral_verification import estimate_alpha

DATA_DIR = "real-data"

def load_series(path):
    df = pd.read_csv(path)
    for col in ["value", "Sunspots", "Close", "price"]:
        if col in df.columns:
            return df[col].values
    raise ValueError(f"No valid column in {path}")

def main():
    results = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            path = os.path.join(DATA_DIR, file)
            try:
                series = load_series(path)
                alpha = estimate_alpha(series)
                results.append((file, alpha))
                print(f"{file}: alpha={alpha}")
            except Exception as e:
                print(f"{file}: FAILED ({e})")

    if len(results) < 2:
        raise SystemExit("❌ Not enough datasets")

    if failed_count > total_count * 0.2:
        raise SystemExit("❌ Too many dataset failures — invariant not stable")

    print("✅ CROSS DOMAIN VALIDATION DONE")

if __name__ == "__main__":
    main()
