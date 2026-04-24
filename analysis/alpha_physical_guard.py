import json
import sys
import os

def load_alpha():
    # Priority 1: real external classification
    if os.path.exists("artifacts/external_classification.json"):
        with open("artifacts/external_classification.json") as f:
            r = json.load(f)
            return r["alpha"], None

    # Fallback: canonical synthetic
    with open("artifacts/canonical_report.json") as f:
        r = json.load(f)
        return r["spectral_profile"]["estimated_alpha"], r["spectral_profile"]["bootstrap_std"]


alpha, sigma = load_alpha()

with open("core-scientific/unified_claim.json") as f:
    claim = json.load(f)

adaptive = claim.get("adaptive_alpha", {})

if "alpha_range" not in adaptive:
    print("❌ Missing adaptive alpha_range")
    sys.exit(1)

alpha_min, alpha_max = adaptive["alpha_range"]

if not (alpha_min <= alpha <= alpha_max):
    print(f"❌ Alpha خارج النطاق التكيفي: {alpha}")
    sys.exit(1)

# sigma optional if external
if sigma is not None:
    if sigma > 0.5:
        print(f"❌ Sigma عالي: {sigma}")
        sys.exit(1)

print("✅ Alpha physically valid (unified source)")
