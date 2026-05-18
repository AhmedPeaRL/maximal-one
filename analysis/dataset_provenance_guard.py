import hashlib
import json
import pandas as pd

DATASETS = [
    "real-data/sunspots_full.csv",
    "real-data/sunspots_global_extended.csv",
    "real-data/white_noise.csv",
    "real-data/random_walk.csv",
    "real-data/shuffled_sunspots.csv"
]

def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)

    return h.hexdigest()

report = {}

for path in DATASETS:
    df = pd.read_csv(path)

    report[path] = {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "sha256": sha256_file(path)
    }

with open(
    "artifacts/dataset_provenance.json",
    "w"
) as f:
    json.dump(
        report,
        f,
        indent=2,
        sort_keys=True
    )

print("✅ DATASET PROVENANCE SEALED")
