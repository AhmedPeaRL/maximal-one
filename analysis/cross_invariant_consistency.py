import json
import numpy as np
import pathlib

ART = pathlib.Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

# ===== load invariants =====

files = [
    "invariant_history.json",
    "universal_invariants.json",
    "scaling_law_test.json"
]

vectors = []

for f in files:
    data = load(f)
    if not data:
        continue

    # نحاول نستخرج أرقام meaningful
    flat = []

    def extract(x):
        if isinstance(x, dict):
            for v in x.values():
                extract(v)
        elif isinstance(x, list):
            for v in x:
                extract(v)
        elif isinstance(x, (int, float)):
            flat.append(float(x))

    extract(data)

    if len(flat) > 5:
        vec = np.array(flat)
        vec = (vec - np.mean(vec)) / (np.std(vec) + 1e-9)
        vectors.append(vec[:100])  # clip

# ===== consistency check =====

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))

scores = []

for i in range(len(vectors)):
    for j in range(i+1, len(vectors)):
        scores.append(cosine(vectors[i], vectors[j]))

result = {
    "num_systems": len(vectors),
    "consistency_scores": scores,
    "mean_consistency": float(np.mean(scores)) if scores else 0,
    "strong_invariant": float(np.mean(scores)) > 0.85 if scores else False
}

(ART / "cross_invariant_consistency.json").write_text(
    json.dumps(result, indent=2)
)

print("==== CROSS INVARIANT CONSISTENCY ====")
print(json.dumps(result, indent=2))
