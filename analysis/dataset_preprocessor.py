import pandas as pd
import sys
import os

def run(file_path):

    df = pd.read_csv(file_path)

    print("==== RAW DATA PREVIEW ====")
    print(df.head())
    print("Columns:", df.columns.tolist())
    print("Shape:", df.shape)

    # 🧠 اختار أول column رقمي فعلاً
    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) == 0:
        print("No numeric columns found — FAIL")
        sys.exit(1)

    col = numeric_cols[0]

    print(f"Using column: {col}")

    series = df[col].dropna()

    print("After dropna:", len(series))

    if len(series) < 200:
        print("Too few data points after cleaning — FAIL")
        sys.exit(1)

    # normalize (optional but safe)
    series = (series - series.mean()) / (series.std() + 1e-8)

    out_path = file_path.replace(".csv", "_prepared.csv")

    series.to_csv(out_path, index=False, header=["value"])

    print(f"Prepared dataset saved: {out_path}")
    print("Final length:", len(series))

if __name__ == "__main__":
    run(sys.argv[1])
