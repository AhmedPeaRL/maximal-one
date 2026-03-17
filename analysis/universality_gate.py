import json
import os
import numpy as np

ARTIFACTS = "artifacts"


def load_features():
    path = os.path.join(ARTIFACTS, "universality_features.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def extract_signal(features):

    vectors = []

    for v in features.values():
        if not isinstance(v, dict):
            continue

        vals = []

        for k in ["mean", "variance", "skewness", "kurtosis"]:
            if k in v:
                try:
                    vals.append(float(v[k]))
                except:
                    vals.append(0.0)

        if vals:
            vectors.append(vals)

    if not vectors:
        return 0.0

    X = np.array(vectors)

    # normalize
    X = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + 1e-8)

    # covariance structure
    cov = np.cov(X.T)

    eigvals = np.linalg.eigvals(cov)
    eigvals = np.real(eigvals)

    total = np.sum(eigvals)

    if total <= 0:
        return 0.0

    # signal strength = dominance of first mode
    signal = np.max(eigvals) / total

    return float(signal)


def main():
    raw = load_features()

    if raw is None:
        result = {"strength": 0.0, "passed": False}
    else:
        if isinstance(raw, list):
            features = {f"f{i}": v for i, v in enumerate(raw)}
        else:
            features = raw

        strength = extract_signal(features)

        result = {
            "strength": strength,
            "passed": strength > 0.25
        }

    os.makedirs(ARTIFACTS, exist_ok=True)

    with open(os.path.join(ARTIFACTS, "global_signal.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
