import json
import random
import statistics
import hashlib

SEED = 42

def main():
    rng = random.Random(SEED)
    data = [rng.random() for _ in range(1000)]

    mean = statistics.mean(data)
    variance = statistics.variance(data)

    state = {
        "seed": SEED,
        "mean": mean,
        "variance": variance
    }

    canonical = json.dumps(state, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()

    output = {
        "sha256": digest,
        "state": state
    }

    print(json.dumps(output, sort_keys=True, separators=(",", ":")))

if __name__ == "__main__":
    main()
