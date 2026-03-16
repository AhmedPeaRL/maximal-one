import json
import numpy as np
from pathlib import Path

INPUT = "artifacts/universality_features.json"
OUT = "artifacts/robust_universality_features.json"


def mad_filter(values):

    median = np.median(values)
    mad = np.median(np.abs(values - median))

    if mad == 0:
        return np.ones(len(values), dtype=bool)

    z = 0.6745 * (values - median) / mad

    return np.abs(z) < 3


def run():

    if not Path(INPUT).exists():
        print("Feature file missing")
        return

    with open(INPUT) as f:
        data = json.load(f)

    records = []

    # case 1 : list format
    if isinstance(data, list):
        records = data

    # case 2 : dict format
    elif isinstance(data, dict):
        for name,vals in data.items():
            r = vals
            r["dataset"] = name
            records.append(r)

    else:
        print("Unknown data format")
        return

    alpha = np.array([
        r.get("spectral_alpha", np.nan) for r in records
    ])

    mask = mad_filter(alpha)

    filtered = []

    for i,r in enumerate(records):
        if mask[i]:
            filtered.append(r)

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:
        json.dump(filtered,f,indent=2)

    print("Filtered systems:",len(filtered))
    print("Original systems:",len(records))


if __name__ == "__main__":
    run()
