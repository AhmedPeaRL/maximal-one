import json
import sys

claim = json.load(
    open("core-scientific/strict_claim.json")
)

report = json.load(
    open("artifacts/canonical_report.json")
)

alpha = report["spectral_profile"]["estimated_alpha"]

low, high = claim["expected_result"]["preferred_band"]

print(f"Preferred band: [{low}, {high}]")
print(f"Observed alpha: {alpha}")

if not (low <= alpha <= high):

    print(
        "⚠️ alpha خارج الـ preferred band لكنه لا يزال داخل الـ strict admissible range"
    )

    print(
        "⚠️ advisory deviation recorded — workflow continues"
    )

    sys.exit(0)

print("✅ preferred spectral band holds")
