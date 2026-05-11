import json

claim = json.load(
    open("core-scientific/strict_claim.json")
)

report = json.load(
    open("artifacts/canonical_report.json")
)

alpha = report["spectral_profile"]["estimated_alpha"]

low, high = claim["expected_result"]["preferred_band"]

if not (low <= alpha <= high):

    print(
        "⚠️ alpha خارج الـ preferred band لكن داخل strict range"
    )

    raise SystemExit(
        "⚠️ Preferred spectral band exceeded"
    )

print("✅ preferred spectral band holds")
