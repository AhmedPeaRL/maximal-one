import json
import sys

try:
    with open("artifacts/canonical_report.json") as f:
        report = json.load(f)

    with open("core-scientific/external_ground_truth.json") as f:
        gt = json.load(f)

except Exception as e:
    print("❌ Missing required files:", e)
    sys.exit(1)

alpha = report.get("spectral_profile", {}).get("estimated_alpha", None)
sigma = report.get("spectral_profile", {}).get("bootstrap_std", None)

if alpha is None:
    print("❌ Missing alpha")
    sys.exit(1)

matched = False
soft_matched = False

for bench in gt["external_benchmarks"]:
    rule = bench["validation_rule"]

    if "spectral_peak_range" in rule:
        low, high = rule["spectral_peak_range"]

        # strict match
        if low <= alpha <= high:
            print(f"✅ STRICT match: {bench['name']}")
            matched = True

        # soft match (with sigma tolerance)
        elif sigma is not None:
            margin = sigma * gt["integration_policy"].get("soft_match_sigma_multiplier", 2.0)

            if (low - margin) <= alpha <= (high + margin):
                print(f"⚠️ SOFT match: {bench['name']} (within uncertainty margin)")
                soft_matched = True

if matched:
    print("✅ External grounding achieved (strict)")
    sys.exit(0)

if alpha > 5:
    print("⚠️ High alpha detected — potential scaling anomaly or new regime")

if soft_matched and gt["integration_policy"].get("allow_soft_match", False):
    print("⚠️ External grounding achieved (soft)")
    sys.exit(0)

if gt["integration_policy"]["failure_if_none_match"]:
    print("❌ No external benchmark matched — model ungrounded")
    sys.exit(1)

print("⚠️ No match but failure disabled")
