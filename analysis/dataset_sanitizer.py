import pandas as pd
import numpy as np
import sys
from pathlib import Path

MIN_ROWS = 200

def sanitize(path):
    try:
        df = pd.read_csv(path)

        # keep only numeric columns
        df = df.select_dtypes(include=[np.number])

        if df.empty:
            print(f"[SKIP] {path} no numeric columns")
            return None

        if len(df) < MIN_ROWS:
            print(f"[SKIP] {path} dataset too small")
            return None

        df = df.dropna()

        if len(df) < MIN_ROWS:
            print(f"[SKIP] {path} too many NaN")
            return None

        return df

    except Exception as e:
        print(f"[ERROR] {path} {e}")
        return None


def main():
    data_dir = Path("real-data")

    for f in data_dir.glob("*.csv"):
        df = sanitize(f)

        if df is None:
            continue

        out = data_dir / (f.stem + "_clean.csv")
        df.to_csv(out, index=False)

        print("[CLEAN]", out)


if __name__ == "__main__":
    main()
