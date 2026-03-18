import json
import numpy as np
import pathlib

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

    if len(nums) < 10:
        continue

    v = np.array(nums)
    v = (v - np.mean(v)) / (np.std(v) + 1e-9)

    # clip ثابت
    v = v[:128]

    if len(v) == 128:
        vectors.append(v)

# ===== pairwise cosine =====

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b)))

scores = []

for i in range(len(vectors)):
    for j in range(i+1, len(vectors)):
        scores.append(cosine(vectors[i], vectors[j]))

result = {
    "num_vectors": len(vectors),
    "pairwise_scores": scores,
    "mean_consistency": float(np.mean(scores)) if scores else 0,
    "strong_field": float(np.mean(scores)) > 0.75 if scores else False
}

(ART / "invariant_field.json").write_text(
    json.dumps(result, indent=2)
)

print("==== INVARIANT FIELD ====")
print(json.dumps(result, indent=2))
