import json
import numpy as np
import pathlib
from sklearn.decomposition import PCA

ART = pathlib.Path("artifacts")

def extract_numbers(obj, acc):
    if isinstance(obj, dict):
        for v in obj.values():
            extract_numbers(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            extract_numbers(v, acc)
    elif isinstance(obj, (int, float)):
        if np.isfinite(obj):  # ✅ filter NaN / inf early
            acc.append(float(obj))

vectors = []

for file in ART.glob("*.json"):
    try:
        data = json.loads(file.read_text())
    except:
        continue

    nums = []
    extract_numbers(data, nums)

    if len(nums) < 20:
        continue

    v = np.array(nums, dtype=np.float64)

    # ✅ remove any residual non-finite values
    v = v[np.isfinite(v)]

    if len(v) < 20:
        continue

    std = np.std(v)

    # ✅ skip degenerate vectors (zero variance)
    if std < 1e-12:
        continue

    v = (v - np.mean(v)) / std

    # ✅ enforce fixed dimension safely
    if len(v) >= 128:
        v = v[:128]
    else:
        continue

    # ✅ final safety check
    if not np.all(np.isfinite(v)):
        continue

    vectors.append(v)

vectors = np.array(vectors, dtype=np.float64)

# ✅ global sanity check
if len(vectors) == 0 or not np.all(np.isfinite(vectors)):
    result = {
        "status": "invalid_vectors",
        "num_vectors": int(len(vectors))
    }

elif len(vectors) < 3:
    result = {
        "status": "not_enough_data",
        "num_vectors": int(len(vectors))
    }

else:
    # ✅ extra guard before PCA
    vectors = vectors[np.all(np.isfinite(vectors), axis=1)]

    if len(vectors) < 3:
        result = {
            "status": "filtered_too_much",
            "num_vectors": int(len(vectors))
        }
    else:
        pca = PCA(n_components=3)
        proj = pca.fit_transform(vectors)

        explained = pca.explained_variance_ratio_

        result = {
            "num_vectors": int(len(vectors)),
            "explained_variance": explained.tolist(),
            "low_dimensional_structure": float(np.sum(explained[:2])) > 0.75
        }

(ART / "invariant_geometry.json").write_text(
    json.dumps(result, indent=2)
)

print("==== INVARIANT GEOMETRY ====")
print(json.dumps(result, indent=2))
