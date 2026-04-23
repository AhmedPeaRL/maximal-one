import glob
import pandas as pd
from analysis.numerical_spectral_verification import estimate_alpha

def scan_all_datasets():
    results = []

    for path in glob.glob("real-data/*.csv"):
        try:
            df = pd.read_csv(path)

            if "value" not in df.columns:
                continue

            alpha = estimate_alpha(df["value"].values)

            results.append({
                "dataset": path,
                "alpha": float(alpha)
            })

        except Exception:
            continue

    return results


if __name__ == "__main__":
    r = scan_all_datasets()

    import json
    with open("artifacts/cross_dataset_scan.json", "w") as f:
        json.dump(r, f, indent=2)

    print("Cross-dataset scan complete:", len(r))
