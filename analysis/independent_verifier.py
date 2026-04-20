import json
import hashlib
import os
import time

def load_report():
    with open("artifacts/canonical_report.json") as f:
        return json.load(f)

def verify_hash():
    with open("artifacts/report.hash") as f:
        stored = f.read().strip()

    with open("artifacts/canonical_report.json","rb") as f:
        calc = hashlib.sha256(f.read()).hexdigest()

    return stored == calc

def external_verdict():
    report = load_report()

    alpha = report["spectral_profile"]["estimated_alpha"]
    sigma = report["spectral_profile"]["bootstrap_std"]

    if sigma > 0.2:
        return "unstable"

    if alpha < 0:
        return "invalid"

    return "coherent"

def build_external_record():
    return {
        "timestamp": time.time(),
        "integrity": verify_hash(),
        "verdict": external_verdict(),
        "source": "independent_layer"
    }

if __name__ == "__main__":
    os.makedirs("public", exist_ok=True)

    record = build_external_record()

    with open("public/independent_verification.json","w") as f:
        json.dump(record, f, indent=2)

    print("Independent verification written.")
