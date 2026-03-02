# analysis/real_data_adapter.py

import numpy as np
import pandas as pd
import json
import hashlib

def load_csv_series(path, column=None):
    df = pd.read_csv(path)

    if column is None:
        column = df.columns[0]

    series = df[column].dropna().values.astype(float)

    return series

def normalize(series):
    series = np.array(series)
    return (series - np.mean(series)) / np.std(series)

def canonical_hash(series):
    payload = np.array(series, dtype=np.float64).tobytes()
    return hashlib.sha256(payload).hexdigest()

def export_series(series, out_path):
    with open(out_path, "w") as f:
        json.dump({
            "length": len(series),
            "hash": canonical_hash(series)
        }, f, sort_keys=True)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python real_data_adapter.py data.csv")
        exit(1)

    path = sys.argv[1]
    series = normalize(load_csv_series(path))
    export_series(series, "artifacts/real_data_signature.json")

    print("Real data signature generated.")
