import json
import sys

with open("artifacts/canonical_report.json") as f:
    r = json.load(f)

alpha = r["spectral_profile"]["estimated_alpha"]
sigma = r["spectral_profile"]["bootstrap_std"]

if not (0 <= alpha <= 3):
    print(f"❌ Alpha خارج النطاق الفيزيائي: {alpha}")
    sys.exit(1)

if sigma > 0.5:
    print(f"❌ Sigma عالي: {sigma}")
    sys.exit(1)

print("✅ Alpha physically valid")
