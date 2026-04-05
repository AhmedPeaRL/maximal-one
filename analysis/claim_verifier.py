import json
import numpy as np
from pathlib import Path

# === LOAD CLAIM ===
with open("core-scientific/minimal_claim.json") as f:
    claim = json.load(f)

# === LOAD RESULTS ===
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

# === CLAIM CRITERIA ===
alpha_min, alpha_max = claim["expected_outcome"]["alpha_range"]
max_dev = claim["test_protocol"]["acceptance_criteria"]["max_deviation"]
confidence = claim["test_protocol"]["acceptance_criteria"]["confidence"]

# === EVALUATION ===
center = (alpha_min + alpha_max) / 2
deviation = abs(alpha - center)

passed_range = alpha_min <= alpha <= alpha_max
passed_deviation = deviation <= max_dev
confidence_est = 1.0 - (std / (abs(alpha) + 1e-8))

passed_confidence = confidence_est >= confidence

final_pass = passed_range and passed_deviation and passed_confidence

# === OUTPUT ===
result = {
    "alpha": alpha,
    "std": std,
    "deviation": deviation,
    "confidence_est": confidence_est,
    "criteria": {
        "range_pass": passed_range,
        "deviation_pass": passed_deviation,
        "confidence_pass": passed_confidence
    },
    "final_pass": final_pass,
    "interpretation": "Invariant confirmed" if final_pass else "Claim not supported"
}

Path("artifacts").mkdir(exist_ok=True)

with open("artifacts/claim_verification.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))

# === HARD FAIL OPTION ===
if not final_pass:
    print("❌ CLAIM FAILED")
    exit(1)
else:
    print("✅ CLAIM VERIFIED")
