import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path("artifacts/phase_space_invariants.json")

def load_series(path):
    df = pd.read_csv(path)

    numeric = df.select_dtypes(include=[np.number])

    if numeric.shape[1] == 0:
        return None

    series = numeric.iloc[:,0].dropna()

    if len(series) < 100:
        return None

    return series.values


def estimate_dimension(x):

    n = len(x)

    diff = np.abs(x[:-1] - x[1:])

    eps = np.std(diff)

    c = np.sum(diff < eps) / n

    if c <= 0:
        return None

    dim = np.log(c) / np.log(eps)

    return float(dim)


def main():

    if len(sys.argv) < 2:
        print("Dataset path required")
        sys.exit(0)

    path = sys.argv[1]

    series = load_series(path)

    if series is None:
        print("Dataset invalid or too small")
        sys.exit(0)

    dim = estimate_dimension(series)

    OUT.parent.mkdir(exist_ok=True)

    with open(OUT,"w") as f:
        json.dump(
            {
                "dataset":path,
                "attractor_dimension":dim
            },
            f,
            indent=2
        )

    print("Phase space invariant saved")


if __name__ == "__main__":
    main()
