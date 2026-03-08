import os
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

DATA_DIR = "real-data"


def lyapunov_estimate(series):

    x = series.values
    n = len(x)

    if n < 100:
        return None

    emb_dim = 3
    delay = 2

    vectors = []

    for i in range(n - emb_dim * delay):
        vec = [x[i + j * delay] for j in range(emb_dim)]
        vectors.append(vec)

    vectors = np.array(vectors)

    nbrs = NearestNeighbors(n_neighbors=2).fit(vectors)
    distances, indices = nbrs.kneighbors(vectors)

    div = []

    for i in range(len(vectors) - 2):

        j = indices[i][1]

        if j + 1 >= len(vectors):
            continue

        d0 = np.linalg.norm(vectors[i] - vectors[j])
        d1 = np.linalg.norm(vectors[i+1] - vectors[j+1])

        if d0 > 0 and d1 > 0:
            div.append(np.log(d1/d0))

    if len(div) == 0:
        return None

    return float(np.mean(div))


def analyze_dataset(path):

    df = pd.read_csv(path)

    if "value" not in df:
        return None

    series = df["value"].dropna()

    if len(series) < 200:
        return None

    lyap = lyapunov_estimate(series)

    return {
        "dataset": os.path.basename(path),
        "lyapunov_estimate": lyap
    }


def main():

    results = []

    for f in os.listdir(DATA_DIR):

        if not f.endswith(".csv"):
            continue

        path = os.path.join(DATA_DIR, f)

        r = analyze_dataset(path)

        if r:
            results.append(r)

    for r in results:
        print(r)


if __name__ == "__main__":
    main()
