import json
import numpy as np
from pathlib import Path

# === LOAD REPORT ===
report_path = Path("artifacts/canonical_report.json")

if not report_path.exists():
    raise RuntimeError("Missing canonical_report.json")

with open(report_path) as f:
    report = json.load(f)

alpha = report.get("spectral_profile", {}).get("estimated_alpha")
std = report.get("spectral_profile", {}).get("bootstrap_std")

if alpha is None or std is None:
    raise RuntimeError("Missing spectral data")

# === ADAPTIVE RANGE ===
k = 2.0  # coverage ~95%

alpha_min = alpha - k * std
alpha_max = alpha + k * std

# === BUILD CLAIM ===
adaptive_claim = {
    "statement": "Adaptive invariant range derived from empirical spectral distribution",
    "expected_outcome": {
        "alpha_range": [float(alpha_min), float(alpha_max)]
    },
    "test_protocol": {
        "acceptance_criteria": {
            "confidence": 0.95
        }
    }
}

Path("artifacts").mkdir(exist_ok=True)

with open("artifacts/adaptive_claim.json", "w") as f:
    json.dump(adaptive_claim, f, indent=2)

print(json.dumps(adaptive_claim, indent=2))
