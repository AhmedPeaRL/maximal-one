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


def normalize_to_dict(data):
    """
    نفس منطق feature_ranking
    """
    if isinstance(data, dict):
        return data

    if isinstance(data, list):
        normalized = {}
        for i, item in enumerate(data):
            if isinstance(item, dict):
                key = item.get("name", f"feature_{i}")
                normalized[key] = item
            else:
                normalized[f"feature_{i}"] = {"value": item}
        return normalized

    return {"unknown": {"value": data}}


def score_feature_stability():
    raw = load_json("universality_features.json")
    if not raw:
        return 0.0

    features = normalize_to_dict(raw)

    scores = []
    for k, v in features.items():
        if isinstance(v, dict):
            var = v.get("variance", None)
            if var is None:
                continue
            try:
                var = float(var)
            except:
                continue

            scores.append(1.0 / (1.0 + var))

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


def identity_coherence():
    """
    يقيس هل عندنا أسماء features حقيقية ولا مجرد feature_0,1,2
    """
    raw = load_json("universality_features.json")
    if not raw:
        return 0.0

    features = normalize_to_dict(raw)

    names = list(features.keys())

    meaningful = [n for n in names if not n.startswith("feature_")]

    if not names:
        return 0.0

    return len(meaningful) / len(names)


def main():
    stability = score_feature_stability()
    consistency = cross_domain_consistency()
    entropy = entropy_signal()
    identity = identity_coherence()

    score = (
        0.4 * stability +
        0.25 * (1.0 / (1.0 + consistency)) +
        0.2 * entropy +
        0.15 * identity
    )

    result = {
        "stability": stability,
        "consistency": consistency,
        "entropy_signal": entropy,
        "identity_coherence": identity,
        "universality_score": score,
        "passed": score > 0.6
    }

    os.makedirs(ARTIFACTS, exist_ok=True)

    with open(os.path.join(ARTIFACTS, "universality_gate.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
