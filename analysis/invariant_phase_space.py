import sys
import json
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

OUTPUT = "artifacts/phase_space_invariants.json"


def correlation_dimension(data, r_vals):
    N = len(data)
    nbrs = NearestNeighbors(radius=max(r_vals)).fit(data)
    corr = []

    for r in r_vals:
        count = 0
        for point in data:
            neighbors = nbrs.radius_neighbors([point], r, return_distance=False)[0]
            count += len(neighbors)

        corr.append(count / (N * N))

    log_r = np.log(r_vals)
    log_c = np.log(corr)

    slope = np.polyfit(log_r, log_c, 1)[0]
    return float(slope)


def attractor_radius(data):
    center = np.mean(data, axis=0)
    dist = np.linalg.norm(data - center, axis=1)
    return float(np.mean(dist))


def entropy_rate(series):
    hist, _ = np.histogram(series, bins=50, density=True)
    hist = hist[hist > 0]
    return float(-np.sum(hist * np.log(hist)))


def main(path):

    df = pd.read_csv(path)

    series = df.iloc[:, 1].values
    embedded = np.column_stack([
        series[:-2],
        series[1:-1],
        series[2:]
    ])

    r_vals = np.logspace(-3, 0, 20)

    dim = correlation_dimension(embedded, r_vals)

    radius = attractor_radius(embedded)

    entropy = entropy_rate(series)

    result = {
        "correlation_dimension": dim,
        "attractor_radius": radius,
        "entropy_rate": entropy
    }

    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
