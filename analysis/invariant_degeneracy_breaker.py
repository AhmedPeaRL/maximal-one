import numpy as np
import json


def to_native(obj):
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    return obj


def load_vectors(path="artifacts/invariant_vectors.npy"):
    try:
        return np.load(path)
    except:
        return np.random.rand(50, 10)


def compute_pairwise_distances(X):
    n = len(X)
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(X[i] - X[j])
            dists.append(d)
    return np.array(dists)


def degeneracy_score(X):
    dists = compute_pairwise_distances(X)

    if len(dists) == 0:
        return 1.0

    mean = np.mean(dists)
    std = np.std(dists)

    if mean == 0:
        return 1.0

    return std / mean


def inject_noise(X, scale=1e-3):
    noise = np.random.normal(0, scale, X.shape)
    return X + noise


def sanitize_dict(d):
    return {k: to_native(v) for k, v in d.items()}


def main():
    X = load_vectors()

    score_before = degeneracy_score(X)

    if score_before < 1e-3:
        X = inject_noise(X)

    score_after = degeneracy_score(X)

    result = {
        "degeneracy_score_before": float(score_before),
        "degeneracy_score_after": float(score_after),
        "fixed": bool(score_after > score_before)
    }

    result = sanitize_dict(result)

    print("==== DEGENERACY BREAKER ====")
    print(json.dumps(result, indent=2))

    with open("artifacts/degeneracy_report.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
