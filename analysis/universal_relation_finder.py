import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

FEATURE_FILE = "artifacts/universality_features.csv"

OUTPUT_FILE = "artifacts/universal_relations.json"

def load_features():

    if not Path(FEATURE_FILE).exists():
        return None

    df = pd.read_csv(FEATURE_FILE)

    if df.empty:
        return None

    return df


def test_relation(x, y):

    X = x.reshape(-1,1)

    model = LinearRegression()

    model.fit(X,y)

    pred = model.predict(X)

    r2 = r2_score(y,pred)

    return {
        "slope": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "r2": float(r2)
    }


def search_relations(df):

    features = [
        "spectral_alpha",
        "entropy_rate",
        "hurst_exponent",
        "attractor_dimension"
    ]

    relations = []

    for i in range(len(features)):
        for j in range(len(features)):

            if i == j:
                continue

            f1 = features[i]
            f2 = features[j]

            sub = df[[f1,f2]].dropna()

            if len(sub) < 6:
                continue

            res = test_relation(
                sub[f1].values,
                sub[f2].values
            )

            if res["r2"] > 0.6:

                relations.append({
                    "relation": f"{f2} ≈ a*{f1} + b",
                    "slope": res["slope"],
                    "intercept": res["intercept"],
                    "r2": res["r2"],
                    "systems": int(len(sub))
                })

    return relations


def main():

    df = load_features()

    if df is None:
        print("No features available")
        return

    relations = search_relations(df)

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(relations,f,indent=2)

    print("Discovered relations:")

    print(json.dumps(relations,indent=2))


if __name__ == "__main__":
    main()
