import json
import numpy as np
import pathlib

ART = pathlib.Path("artifacts")

def safe_get(d, path, default=0.0):
    try:
        for p in path:
            d = d[p]
        return float(d)
    except:
        return default

def build_feature_vector(data):
    return np.array([
        # spectral
        safe_get(data, ["spectral_profile", "estimated_alpha"]),
        safe_get(data, ["spectral_profile", "bootstrap_std"]),

        # chaos
        safe_get(data, ["lyapunov", "value"]),
        safe_get(data, ["entropy", "value"]),

        # temporal
        safe_get(data, ["temporal", "dominance"]),
        safe_get(data, ["temporal", "stability"]),

        # universality
        safe_get(data, ["universality", "score"]),
        safe_get(data, ["universality", "confidence"]),

        # predictive
        safe_get(data, ["predictive", "gain"]),
        safe_get(data, ["predictive", "error"]),

        # geometry proxies
        safe_get(data, ["invariant", "density"]),
        safe_get(data, ["invariant", "consistency"])
    ])

vectors = []

for file in ART.glob("*.json"):
    try:
        data = json.loads(file.read_text())
    except:
        continue

    vec = build_feature_vector(data)

    if np.any(np.isnan(vec)):
        continue

    vectors.append(vec)

vectors = np.array(vectors)

if len(vectors) < 3:
    result = {
        "status": "not_enough_data",
        "num_vectors": len(vectors)
    }
else:
    # normalize
    mean = np.mean(vectors, axis=0)
    std = np.std(vectors, axis=0) + 1e-9
    vectors = (vectors - mean) / std

    # covariance spectrum
    cov = np.cov(vectors.T)
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.flip(np.sort(eigvals))

    explained = eigvals / np.sum(eigvals)

    result = {
        "num_vectors": int(len(vectors)),
        "explained_variance": explained[:5].tolist(),
        "low_dimensional_structure": float(np.sum(explained[:2])) > 0.75
    }

(ART / "invariant_embedding.json").write_text(
    json.dumps(result, indent=2)
)

print("==== INVARIANT EMBEDDING ====")
print(json.dumps(result, indent=2))
