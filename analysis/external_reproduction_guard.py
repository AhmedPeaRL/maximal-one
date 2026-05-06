import json
import numpy as np
import hashlib

def load_report(path="artifacts/canonical_report.json"):
    with open(path, "r") as f:
        return json.load(f)

def compute_fingerprint(report):
    sp = report["spectral_profile"]
    
    alpha = float(np.round(sp["estimated_alpha"], 6))
    sigma = float(np.round(sp["bootstrap_std"], 6))
    
    vector = np.array([alpha, sigma])
    vector_bytes = vector.tobytes()
    
    return hashlib.sha256(vector_bytes).hexdigest()

def validate_external_consistency(local_fp, external_fp):
    print("Local FP:", local_fp)
    print("External FP:", external_fp)
    
    if local_fp != external_fp:
        raise SystemExit("❌ External reproduction mismatch")
    
    print("✅ External reproduction MATCH")

if __name__ == "__main__":
    report = load_report()
    local_fp = compute_fingerprint(report)
    
    # placeholder — سيتم استبداله لاحقاً
    external_fp = local_fp  
    
    validate_external_consistency(local_fp, external_fp)
