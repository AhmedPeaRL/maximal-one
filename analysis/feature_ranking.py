import json
import os

ARTIFACTS = "artifacts"

def main():
    path = os.path.join(ARTIFACTS, "universality_features.json")
    
    if not os.path.exists(path):
        print("No features found")
        return
    
    with open(path) as f:
        data = json.load(f)

    ranking = []

    for k, v in data.items():
        if isinstance(v, dict):
            var = v.get("variance", 1.0)
            score = 1.0 / (1.0 + var)
            ranking.append((k, score))

    ranking.sort(key=lambda x: x[1], reverse=True)

    result = {k: float(s) for k, s in ranking}

    with open(os.path.join(ARTIFACTS, "feature_ranking.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
