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

    v = np.array(nums)
    v = (v - np.mean(v)) / (np.std(v) + 1e-9)

    v = v[:128]
    if len(v) == 128:
        vectors.append(v)

vectors = np.array(vectors)

if len(vectors) < 3:
    result = {
        "status": "not_enough_data",
        "num_vectors": len(vectors)
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
