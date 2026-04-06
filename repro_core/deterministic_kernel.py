import random
import json
import hashlib

from global_reproducibility_guard import enforce_global_determinism

SEED = 42
N = 1000

def compute_state(seed: int, n: int):
    rng = random.Random(seed)
    data = [rng.random() for _ in range(n)]

    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n

    # Canonical float stabilization boundary
    mean = round(mean, 12)
    variance = round(variance, 12)

    return {
        "seed": seed,
        "mean": mean,
        "variance": variance,
    }

state = compute_state(SEED, N)

canonical_bytes = json.dumps(state, sort_keys=True).encode()
sha = hashlib.sha256(canonical_bytes).hexdigest()

output = {
    "sha256": sha,
    "state": state,
}

print(json.dumps(output, sort_keys=True))
