import json
from pathlib import Path
import numpy as np

CURRENT = "artifacts/universality_features.json"
HISTORY = "artifacts/invariant_stability_history.json"

def load_current():

    if not Path(CURRENT).exists():
        return []

    with open(CURRENT) as f:
        data = json.load(f)

    if isinstance(data, dict):
        return list(data.values())

    return data


def load_history():

    if not Path(HISTORY).exists():
        return []

    with open(HISTORY) as f:
        return json.load(f)


def save_history(history):

    Path("artifacts").mkdir(exist_ok=True)

    with open(HISTORY,"w") as f:
        json.dump(history,f,indent=2)


def extract_alpha(records):

    alpha = []

    for r in records:
        if "spectral_alpha" in r:
            alpha.append(r["spectral_alpha"])

    return np.array(alpha)


def main():

    records = load_current()
    history = load_history()

    alpha = extract_alpha(records)

    if len(alpha) == 0:
        print("No alpha values found")
        return

    snapshot = {
        "mean_alpha": float(np.mean(alpha)),
        "std_alpha": float(np.std(alpha)),
        "systems": int(len(alpha))
    }

    history.append(snapshot)

    save_history(history)

    print("Recorded snapshot:", snapshot)

    if len(history) > 3:

        means = np.array([h["mean_alpha"] for h in history])

        drift = np.std(means)

        print("Alpha drift:", drift)

        if drift < 0.15:
            print("Invariant stability emerging")
        else:
            print("Invariant still unstable")


if __name__ == "__main__":
    main()
