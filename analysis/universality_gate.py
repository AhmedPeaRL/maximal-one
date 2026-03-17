import json
import os
import numpy as np

ARTIFACTS = "artifacts"

def load_json(name):
    path = os.path.join(ARTIFACTS, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)

def score_feature_stability():
    features = load_json("universality_features.json")
    if not features:
        return 0.0
    
    scores = []
    for k, v in features.items():
        if isinstance(v, dict) and "variance" in v:
            scores.append(1.0 / (1.0 + v["variance"]))
    
    if not scores:
        return 0.0
    
    return float(np.mean(scores))

def cross_domain_consistency():
    clusters = load_json("universality_clusters.json")
    if not clusters:
        return 0.0
    
    sizes = [len(c) for c in clusters if isinstance(c, list)]
    if not sizes:
        return 0.0
    
    return float(np.std(sizes))

def entropy_signal():
    signal = load_json("global_signal.json")
    if not signal:
        return 0.0
    
    return float(signal.get("strength", 0.0))

def main():
    stability = score_feature_stability()
    consistency = cross_domain_consistency()
    entropy = entropy_signal()

    score = (0.5 * stability) + (0.3 * (1.0 / (1.0 + consistency))) + (0.2 * entropy)

    result = {
        "stability": stability,
        "consistency": consistency,
        "entropy_signal": entropy,
        "universality_score": score,
        "passed": score > 0.6
    }

    os.makedirs(ARTIFACTS, exist_ok=True)
    with open(os.path.join(ARTIFACTS, "universality_gate.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
