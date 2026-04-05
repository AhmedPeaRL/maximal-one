import json
import numpy as np
from pathlib import Path

# === LOAD CLAIM ===
with open("core-scientific/minimal_claim.json") as f:
    claim = json.load(f)

# === LOAD REPORT ===
report_path = Path("artifacts/canonical_report.json")

if not report_path.exists():
    raise RuntimeError("Missing canonical_report.json")

with open(report_path) as f:
    report = json.load(f)

# === EXTRACT VALUES ===
alpha = report.get("spectral_profile", {}).get("estimated_alpha")
std = report.get("spectral_profile", {}).get("bootstrap_std")

if alpha is None or std is None:
    raise RuntimeError("Missing spectral data in report")

# === CLAIM PARAMETERS ===
alpha_min, alpha_max = claim["expected_outcome"]["alpha_range"]
confidence_threshold = claim["test_protocol"]["acceptance_criteria"]["confidence"]

# === PROBABILISTIC CHECK ===
# simulate Gaussian around estimated alpha
samples = np.random.normal(loc=alpha, scale=std, size=10000)

within_range = np.logical_and(samples >= alpha_min, samples <= alpha_max)
probability = np.mean(within_range)

# === FINAL DECISION ===
passed_probability = probability >= confidence_threshold

result = {
    "alpha": alpha,
    "std": std,
    "probability_in_range": float(probability),
    "confidence_threshold": confidence_threshold,
    "criteria": {
        "probability_pass": passed_probability
    },
    "final_pass": passed_probability,
    "interpretation": "Invariant confirmed (probabilistic)" if passed_probability else "Claim not supported"
}

Path("artifacts").mkdir(exist_ok=True)

with open("artifacts/claim_verification.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))

# === HARD FAIL ===
if not passed_probability:
    print("❌ CLAIM FAILED")
    exit(1)
else:
    print("✅ CLAIM VERIFIED")
