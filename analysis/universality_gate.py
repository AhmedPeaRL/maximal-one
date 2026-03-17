import json
import os
import numpy as np

ARTIFACTS = "artifacts"


def load_signal():
    path = os.path.join(ARTIFACTS, "global_signal.json")
    if not os.path.exists(path):
        return None

    with open(path) as f:
        return json.load(f)


def compute_strength(signal_data):

    if "features" not in signal_data:
        return 0.0

    stable = signal_data.get("stable_features", [])

    if not stable:
        return 0.0

    # strength = how strong stability is
    cvs = [f["cv"] for f in stable if "cv" in f]

    if not cvs:
        return 0.0

    mean_cv = np.mean(cvs)

    # invert CV → lower CV = stronger signal
    strength = 1.0 / (1.0 + mean_cv)

    return float(strength)


def main():

    signal = load_signal()

    if signal is None:
        result = {
            "strength": 0.0,
            "passed": False,
            "note": "missing_signal"
        }
    else:
        strength = compute_strength(signal)

        result = {
            "strength": strength,
            "passed": strength > 0.4,
            "stable_count": len(signal.get("stable_features", [])),
            "note": "ok" if strength > 0 else "weak"
        }

    os.makedirs(ARTIFACTS, exist_ok=True)

    with open(os.path.join(ARTIFACTS, "universality_gate.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
