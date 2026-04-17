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

if alpha is None:
    print("❌ Missing alpha")
    sys.exit(1)

matched = False

for bench in gt["external_benchmarks"]:
    rule = bench["validation_rule"]

    if "spectral_peak_range" in rule:
        low, high = rule["spectral_peak_range"]
        if low <= alpha <= high:
            print(f"✅ Matched benchmark: {bench['name']}")
            matched = True

if not matched and gt["integration_policy"]["failure_if_none_match"]:
    print("❌ No external benchmark matched — model ungrounded")
    sys.exit(1)

print("✅ External grounding achieved")
