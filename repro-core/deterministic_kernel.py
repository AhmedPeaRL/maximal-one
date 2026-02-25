import json
import hashlib
import random
import platform
import sys

SEED = 42

def nonlinear_transform(x):
    return x**3 - 2*x**2 + 0.5*x + 1

def compute_state(seed=SEED):
    random.seed(seed)
    values = [random.random() for _ in range(1000)]
    transformed = [nonlinear_transform(v) for v in values]

    mean = sum(transformed)/len(transformed)
    variance = sum((v-mean)**2 for v in transformed)/len(transformed)

    return {
        "seed": seed,
        "mean": mean,
        "variance": variance,
        "python_version": platform.python_version(),
        "platform": platform.platform()
    }

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))

def main():
    state = compute_state()
    serialized = canonical_json(state)
    sha = hashlib.sha256(serialized.encode()).hexdigest()

    output = {
        "state": state,
        "sha256": sha
    }

    print(canonical_json(output))

if __name__ == "__main__":
    main()
