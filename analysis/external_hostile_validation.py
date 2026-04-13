import json
import numpy as np
import random

def generate_adversarial_noise(n=1000):
    return np.random.normal(0, 1, n)

def destroy_temporal_structure(series):
    shuffled = series.copy()
    random.shuffle(shuffled)
    return shuffled

def inject_false_signal(series):
    fake = series.copy()
    for i in range(len(fake)):
        fake[i] += np.sin(i * 0.1) * 0.5
    return fake

def run_hostile_tests():
    base = generate_adversarial_noise()

    tests = {
        "pure_noise": base,
        "shuffled_noise": destroy_temporal_structure(base.tolist()),
        "fake_signal": inject_false_signal(base.tolist())
    }

    results = {}

    for name, data in tests.items():
        mean = float(np.mean(data))
        std = float(np.std(data))

        results[name] = {
            "mean": mean,
            "std": std,
            "passed": abs(mean) < 0.1 and std < 2
        }

    with open("artifacts/hostile_validation.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Hostile validation complete")

if __name__ == "__main__":
    run_hostile_tests()
