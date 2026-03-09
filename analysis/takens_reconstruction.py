import sys
import numpy as np
import pandas as pd
import json
import os


def takens_embedding(series, delay=5, dim=3):

    n = len(series)

    embedded = []

    for i in range(n - delay * dim):
        vec = [series[i + j * delay] for j in range(dim)]
        embedded.append(vec)

    return np.array(embedded)


def main():

    path = sys.argv[1]

    df = pd.read_csv(path)

    col = df.columns[0]

    series = df[col].values

    emb = takens_embedding(series)

    os.makedirs("artifacts", exist_ok=True)

    out = {
        "points": len(emb),
        "dimension": 3,
        "delay": 5
    }

    with open("artifacts/takens.json", "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out))


if __name__ == "__main__":
    main()
