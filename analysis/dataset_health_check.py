import pandas as pd
import os
import json

DATA_DIR = "real-data"


def inspect_dataset(path):

    report = {
        "file": path,
        "rows": 0,
        "columns": 0,
        "numeric_columns": 0,
        "missing_ratio": 0.0
    }

    try:
        df = pd.read_csv(path)

    except Exception:
        report["error"] = "unreadable"
        return report

    report["rows"] = len(df)
    report["columns"] = len(df.columns)

    numeric = df.select_dtypes(include="number")

    report["numeric_columns"] = len(numeric.columns)

    report["missing_ratio"] = float(df.isna().mean().mean())

    return report


def main():

    results = []

    for f in os.listdir(DATA_DIR):

        if not f.endswith(".csv"):
            continue

        path = os.path.join(DATA_DIR, f)

        r = inspect_dataset(path)

        results.append(r)

    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/dataset_health.json","w") as f:
        json.dump(results,f,indent=2)

    print(json.dumps(results,indent=2))


if __name__ == "__main__":
    main()
