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

    names = list(data.keys())

    alpha = np.array([data[n]["spectral_alpha"] for n in names])

    mask = mad_filter(alpha)

    filtered = {}

    for i,name in enumerate(names):
        if mask[i]:
            filtered[name] = data[name]

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:
        json.dump(filtered,f,indent=2)

    print("Filtered systems:",len(filtered))
    print("Original systems:",len(names))


if __name__ == "__main__":
    run()
