import json
import sys

with open("artifacts/canonical_report.json") as f:
    r = json.load(f)

alpha = r["spectral_profile"]["estimated_alpha"]

if alpha > 5:
    print("⚠️ Alpha unusually high — flagging for review")
    sys.exit(0)

if alpha < 0:
    print("❌ Invalid alpha")
    sys.exit(1)

print("✅ Alpha sanity OK")
