import pandas as pd
import numpy as np
import json
from pathlib import Path

FEATURE_FILE = "artifacts/universality_features.csv"
OUT = "artifacts/universal_signatures.json"


def find_signatures(df):

    feats = [
        "spectral_alpha",
        "entropy_rate",
        "hurst_exponent",
        "attractor_dimension"
    ]

    signatures = []

    for f in feats:

        vals = df[f].dropna()

        if len(vals) < 6:
            continue

        mean = np.mean(vals)
        std = np.std(vals)

        if std == 0:
            continue

        cv = std / abs(mean)

        signatures.append({
            "feature": f,
            "mean": float(mean),
            "std": float(std),
            "coefficient_of_variation": float(cv),
            "systems": int(len(vals))
        })

    signatures.sort(key=lambda x: x["coefficient_of_variation"])

    return signatures


def main():

    if not Path(FEATURE_FILE).exists():
        print("No feature file")
        return

    df = pd.read_csv(FEATURE_FILE)

    sig = find_signatures(df)

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUT,"w") as f:
        json.dump(sig,f,indent=2)

    print("Universal signature candidates:")
    print(json.dumps(sig,indent=2))


if __name__ == "__main__":
    main()
