import json
import sys

with open("artifacts/canonical_report.json") as f:
    r = json.load(f)

alpha = r["spectral_profile"]["estimated_alpha"]
sigma = r["spectral_profile"]["bootstrap_std"]

with open("core-scientific/unified_claim.json") as f:
    claim = json.load(f)

alpha_min, alpha_max = claim["adaptive_alpha"]["alpha_range"]

if not (alpha_min <= alpha <= alpha_max):
    print(f"❌ Alpha خارج النطاق التكيفي: {alpha}")
    sys.exit(1)

if sigma > 0.5:
    print(f"❌ Sigma عالي: {sigma}")
    sys.exit(1)

print("✅ Alpha physically valid")
