import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import json
import os

def takens_embedding(series, delay=10, dimension=3):
    N = len(series) - delay*(dimension-1)
    if N <= 0:
        raise ValueError("Series too short for embedding")

    emb = np.zeros((N, dimension))
    for i in range(dimension):
        emb[:,i] = series[i*delay:i*delay+N]

    return emb

def estimate_dimension(data, max_dim=10):
    dims = []
    for d in range(2, max_dim):
        emb = takens_embedding(data, delay=5, dimension=d)
        nbrs = NearestNeighbors(n_neighbors=2).fit(emb)
        dist, _ = nbrs.kneighbors(emb)
        dims.append(np.mean(dist[:,1]))
    return dims

def run(dataset):
    df = pd.read_csv(dataset)

    col = df.columns[1]
    series = df[col].values

    emb = takens_embedding(series, delay=10, dimension=3)

    dim_profile = estimate_dimension(series)

    result = {
        "embedding_points": int(len(emb)),
        "dimension_profile": [float(x) for x in dim_profile]
    }

    os.makedirs("artifacts",exist_ok=True)

    with open("artifacts/takens.json","w") as f:
        json.dump(result,f)

if __name__=="__main__":
    import sys
    run(sys.argv[1])
