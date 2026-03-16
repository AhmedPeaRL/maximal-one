import json
import numpy as np
from pathlib import Path

FEATURE_FILE = "artifacts/universality_features.json"
OUTPUT_FILE = "artifacts/universality_map.json"

def load_features():

    if not Path(FEATURE_FILE).exists():
        print("No universality features file found.")
        return []

    with open(FEATURE_FILE) as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = list(data.values())

    return data


def build_vectors(records):

    vectors = []
    labels = []

    for r in records:

        alpha = r.get("spectral_alpha")
        lyap = r.get("lyapunov")
        hurst = r.get("hurst")

        if alpha is None:
            continue

        vec = [
            float(alpha),
            float(lyap) if lyap is not None else 0.0,
            float(hurst) if hurst is not None else 0.0
        ]

        vectors.append(vec)
        labels.append(r.get("system","unknown"))

    return np.array(vectors), labels


def pairwise_distance_matrix(X):

    n = len(X)
    D = np.zeros((n,n))

    for i in range(n):
        for j in range(n):
            D[i,j] = np.linalg.norm(X[i]-X[j])

    return D


def main():

    records = load_features()

    if not records:
        print("No records available.")
        return

    X, labels = build_vectors(records)

    if len(X) < 2:
        print("Not enough systems for map.")
        return

    D = pairwise_distance_matrix(X)

    result = {
        "systems": labels,
        "distance_matrix": D.tolist(),
        "count": len(labels)
    }

    Path("artifacts").mkdir(exist_ok=True)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(result,f,indent=2)

    print("Universality map built for",len(labels),"systems")


if __name__ == "__main__":
    main()
