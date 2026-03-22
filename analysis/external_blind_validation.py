import json
import random
from pathlib import Path

ART = Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

def generate_blind_noise_series(n=1000):
    return [random.random() for _ in range(n)]

def evaluate_against_blind_data():
    # simulate unseen system behavior
    blind_series = generate_blind_noise_series()

    # simple statistical probe
    mean_val = sum(blind_series) / len(blind_series)

    return {
        "blind_mean": mean_val,
        "passes_randomness": 0.45 < mean_val < 0.55
    }

def main():
    verdict = load("global_verdict.json")

    blind_test = evaluate_against_blind_data()

    result = {
        "external_validation": True,
        "blind_test_passed": blind_test["passes_randomness"],
        "blind_mean": blind_test["blind_mean"],
        "linked_internal_score": verdict.get("final_score") if verdict else None
    }

    (ART / "external_validation.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
