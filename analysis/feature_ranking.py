import json
import os

ARTIFACTS = "artifacts"


def normalize_to_dict(data):
    """
    Ensures data is always converted to a dict-like structure.
    Supports:
    - dict مباشرة
    - list of dicts
    - list of (key,value)
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

    # fallback
    return {"unknown": {"value": data}}


def main():
    path = os.path.join(ARTIFACTS, "universality_features.json")

    if not os.path.exists(path):
        print("No features found")
        return

    with open(path) as f:
        raw_data = json.load(f)

    data = normalize_to_dict(raw_data)

    ranking = []

    for k, v in data.items():
        if isinstance(v, dict):
            var = v.get("variance", 1.0)
            try:
                var = float(var)
            except:
                var = 1.0

            score = 1.0 / (1.0 + var)
            ranking.append((k, score))

    ranking.sort(key=lambda x: x[1], reverse=True)

    result = {k: float(s) for k, s in ranking}

    os.makedirs(ARTIFACTS, exist_ok=True)

    with open(os.path.join(ARTIFACTS, "feature_ranking.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps({
        "status": "ok",
        "num_features": len(result),
        "top_feature": ranking[0][0] if ranking else None
    }, indent=2))


if __name__ == "__main__":
    main()
