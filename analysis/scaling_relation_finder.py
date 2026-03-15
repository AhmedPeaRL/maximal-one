import json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import linregress

FEATURE_FILE = "artifacts/universality_features.csv"
OUTPUT_FILE = "artifacts/scaling_relations.json"


def load_features():

    if not Path(FEATURE_FILE).exists():
        return None

    df = pd.read_csv(FEATURE_FILE)

    if df.empty:
        return None

    return df


def power_law_fit(x,y):

    x = np.array(x)
    y = np.array(y)

    mask = (x > 0) & (y > 0)

    x = x[mask]
    y = y[mask]

    if len(x) < 6:
        return None

    lx = np.log(x)
    ly = np.log(y)

    slope, intercept, r, p, stderr = linregress(lx,ly)

    return {
        "exponent": float(slope),
        "coefficient": float(np.exp(intercept)),
        "r2": float(r**2),
        "samples": int(len(x))
    }


def search_scaling(df):

    features = [
        "spectral_alpha",
        "entropy_rate",
        "hurst_exponent",
        "attractor_dimension"
    ]

    relations = []

    for f1 in features:
        for f2 in features:

            if f1 == f2:
                continue

            sub = df[[f1,f2]].dropna()

            if len(sub) < 6:
                continue

            res = power_law_fit(
                sub[f1].values,
                sub[f2].values
            )

            if res and res["r2"] > 0.6:

                relations.append({
                    "relation": f"{f2} ≈ a*{f1}^k",
                    "exponent": res["exponent"],
                    "coefficient": res["coefficient"],
                    "r2": res["r2"],
                    "systems": res["samples"]
                })

    return relations


def main():

    df = load_features()

    if df is None:
        print("No feature file")
        return

    relations = search_scaling(df)

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(relations,f,indent=2)

    print("Scaling relations discovered:")
    print(json.dumps(relations,indent=2))


if __name__ == "__main__":
    main()
