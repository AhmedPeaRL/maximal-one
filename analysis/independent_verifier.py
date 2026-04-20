import json
import hashlib
import os
import time

def load_json(path):
    with open(path) as f:
        return json.load(f)

def verify_hash():
    with open("artifacts/report.hash") as f:
        stored = f.read().strip()

    with open("artifacts/canonical_report.json","rb") as f:
        calc = hashlib.sha256(f.read()).hexdigest()

    return stored == calc

def external_verdict():
    report = load_json("artifacts/canonical_report.json")
    claim = load_json("core-scientific/one_claim_to_break.json")

    alpha = report["spectral_profile"]["estimated_alpha"]
    sigma = report["spectral_profile"]["bootstrap_std"]

    minA, maxA = claim["claim"]["testable_prediction"]["alpha_range"]
    max_sigma = claim["claim"]["testable_prediction"]["max_sigma"]

    if sigma > max_sigma:
        return "rejected_sigma"

    if not (minA <= alpha <= maxA):
        return "rejected_alpha"

    if sigma < max_sigma * 0.5:
        return "high_confidence"

    return "provisionally_valid"

def build_external_record():
    return {
        "timestamp": time.time(),
        "integrity": verify_hash(),
        "verdict": external_verdict(),
        "source": "independent_layer",
        "mode": "claim_bound"
    }

if __name__ == "__main__":
    os.makedirs("public", exist_ok=True)

    record = build_external_record()

    with open("public/independent_verification.json","w") as f:
        json.dump(record, f, indent=2)

    print("Independent verification (claim-bound) written.")
