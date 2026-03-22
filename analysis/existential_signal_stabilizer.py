import json
import numpy as np
from pathlib import Path

ART = Path("artifacts")

TARGET = [
    "entropy_rate",
    "alpha",
    "hurst_exponent",
    "spectral_alpha",
    "attractor_dimension"
]

def load_signal():
    p = ART / "global_signal.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())

def stabilize(features):
    stabilized = []

    for f in features:
        if f["samples"] < 10:
            continue

        weight = np.log1p(f["samples"])
        stability_score = (1 / (f["cv"] + 1e-6)) * weight

        stabilized.append({
            "feature": f["feature"],
            "stability_score": stability_score,
            "cv": f["cv"],
            "samples": f["samples"]
        })

    return sorted(stabilized, key=lambda x: -x["stability_score"])

def main():
    data = load_signal()
    if not data:
        print(json.dumps({"passed": False, "reason": "no signal"}))
        return

    stabilized = stabilize(data["features"])

    strong = [f for f in stabilized if f["stability_score"] > 2.0]

    result = {
        "stabilized_features": stabilized,
        "strong_count": len(strong),
        "passed": len(strong) >= 2
    }

    (ART / "existential_signal.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
