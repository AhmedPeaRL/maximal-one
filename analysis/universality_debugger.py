import json
import os

ARTIFACTS = "artifacts"

FILES = [
    "universality_features.json",
    "universality_clusters.json",
    "global_signal.json"
]


def inspect_file(name):
    path = os.path.join(ARTIFACTS, name)

    if not os.path.exists(path):
        return {"exists": False}

    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        return {"exists": True, "error": str(e)}

    info = {
        "exists": True,
        "type": type(data).__name__
    }

    if isinstance(data, dict):
        info["keys"] = list(data.keys())[:5]
        info["size"] = len(data)

    elif isinstance(data, list):
        info["length"] = len(data)
        info["sample"] = data[:2]

    return info


def main():
    report = {}

    for f in FILES:
        report[f] = inspect_file(f)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
