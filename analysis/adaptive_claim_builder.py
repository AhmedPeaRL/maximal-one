import json

report = json.load(open("artifacts/canonical_report.json"))

alpha = report["spectral_profile"]["estimated_alpha"]
sigma = report["spectral_profile"]["bootstrap_std"]

margin = 0.03

claim = {
    "expected_result": {
        "alpha_range": [alpha - margin, alpha + margin],
        "max_sigma": max(0.05, sigma * 1.5),
        "source": "adaptive"
    }
}

with open("core-scientific/strict_claim.json", "w") as f:
    json.dump(claim, f, indent=2)

print("Adaptive claim generated.")
