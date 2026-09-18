import json
import os
import sys

import numpy as np

PATH = "data/decision_lineage.json"
OUTPUT = "artifacts/self_drift.json"

def compute_drift():
    os.makedirs("artifacts", exist_ok=True)

    if not os.path.exists(PATH):
        result = {
            "status": "not_evaluable",
            "reason": "no_decision_lineage",
            "samples": 0
        }

        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(json.dumps(result, indent=2))
        return 2

    try:
        with open(PATH, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        result = {
            "status": "not_evaluable",
            "reason": "invalid_lineage",
            "error": type(exc).__name__,
            "message": str(exc)
        }

        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(json.dumps(result, indent=2))
        return 2

    if not isinstance(data, list) or len(data) < 5:
        result = {
            "status": "not_evaluable",
            "reason": "insufficient_lineage",
            "samples": len(data) if isinstance(data, list) else 0
        }

        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(json.dumps(result, indent=2))
        return 2

    try:
        hashes = [
            int(str(d["fingerprint"])[:8], 16)
            for d in data
        ]
    except Exception as exc:
        result = {
            "status": "not_evaluable",
            "reason": "invalid_fingerprint_data",
            "error": type(exc).__name__,
            "message": str(exc)
        }

        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(json.dumps(result, indent=2))
        return 2

    diffs = np.diff(
        np.asarray(hashes, dtype=np.float64)
    )

    drift = float(np.std(diffs))

    result = {
        "status": "evaluated",
        "drift_score": drift,
        "samples": len(hashes),
        "scientific_claim": False,
        "interpretation": (
            "Diagnostic lineage drift only; "
            "no scientific truth claim."
        )
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

    return 0

if __name__ == "__main__":
    sys.exit(compute_drift())
