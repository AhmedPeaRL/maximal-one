import json
import os
import itertools
import numpy as np

DATA_DIR = "data"

def load_results():
    results = []
    for f in os.listdir(DATA_DIR):
        if f.endswith(".json"):
            try:
                with open(os.path.join(DATA_DIR,f)) as fh:
                    results.append(json.load(fh))
            except:
                pass
    return results

def extract_features(results):
    feats = []
    for r in results:
        if "spectral_profile" in r:
            feats.append({
                "alpha": r["spectral_profile"].get("estimated_alpha"),
                "entropy": r.get("entropy"),
                "dataset": r.get("dataset","unknown")
            })
    return feats

def discover_correlations(features):
    hypotheses = []

    for a,b in itertools.combinations(features,2):
        if a["alpha"] and b["alpha"]:
            diff = abs(a["alpha"] - b["alpha"])

            if diff < 0.05:
                hypotheses.append({
                    "type":"spectral_alignment",
                    "datasets":[a["dataset"],b["dataset"]],
                    "alpha_mean":np.mean([a["alpha"],b["alpha"]])
                })

    return hypotheses

def save_hypotheses(h):
    os.makedirs("artifacts",exist_ok=True)
    with open("artifacts/hypotheses.json","w") as f:
        json.dump(h,f,indent=2)

if __name__ == "__main__":
    r = load_results()
    f = extract_features(r)
    h = discover_correlations(f)
    save_hypotheses(h)

    print("Generated hypotheses:",len(h))
