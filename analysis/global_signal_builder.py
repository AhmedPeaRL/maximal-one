import json
import os
import numpy as np

ARTIFACTS = "artifacts"


def load(name):
    path = os.path.join(ARTIFACTS, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def compute_signal():
    temporal = load("temporal_dominance.json")
    structural = load("structural_advantage.json")
    predictive = load("global_verdict.json")

    score = 0.0

    if temporal and temporal.get("temporal_signal"):
        score += 0.3

    if structural and structural.get("structure_preserved"):
        score += 0.3

    if predictive and predictive.get("predictive_pass"):
        score += 0.4

    return score


def main():
    score = compute_signal()

    result = {
        "signal_strength": score,
        "passed": score > 0.5,
        "note": "ok" if score > 0 else "weak"
    }

    os.makedirs(ARTIFACTS, exist_ok=True)

    with open(os.path.join(ARTIFACTS, "global_signal.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
