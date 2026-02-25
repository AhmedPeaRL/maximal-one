import json
import random
import statistics
import hashlib

SEED = 42
N = 1000

def main():
    rng = random.Random(SEED)
    data = [rng.random() for _ in range(N)]

    mean = sum(data) / N
    variance = sum((x - mean) ** 2 for x in data) / N

    # Canonical float stabilization
mean = round(mean, 12)
variance = round(variance, 12)

payload = {
    "seed": SEED,
    "mean": mean,
    "variance": variance,
}

sha = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

output = {
    "sha256": sha,
    "state": payload,
}

print(json.dumps(output, sort_keys=True))

if __name__ == "__main__":
    main()
