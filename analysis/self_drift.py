import json, os, numpy as np

PATH = "data/decision_lineage.json"

def compute_drift():
    if not os.path.exists(PATH):
        print("No lineage yet")
        return

    with open(PATH) as f:
        data = json.load(f)

    if len(data) < 5:
        print("Not enough data for drift")
        return

    hashes = [int(d["fingerprint"][:8], 16) for d in data]

    diffs = np.diff(hashes)
    drift = np.std(diffs)

    result = {
        "drift_score": float(drift),
        "samples": len(hashes)
    }

    with open("artifacts/self_drift.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Drift score:", drift)

if __name__ == "__main__":
    compute_drift()
