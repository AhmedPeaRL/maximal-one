import json
import numpy as np

CLAIM = "core-scientific/strict_claim.json"
THEORY = "core-scientific/theoretical_constraints.json"
REPORT = "artifacts/canonical_report.json"

claim = json.load(open(CLAIM))
theory = json.load(open(THEORY))
report = json.load(open(REPORT))

alpha = report["spectral_profile"]["estimated_alpha"]

lower, upper = claim["expected_result"]["alpha_range"]

if not np.isfinite(alpha):
    raise SystemExit("❌ non-finite alpha")

if alpha < lower:
    raise SystemExit("❌ alpha violates lower theoretical bound")

if alpha > upper:
    raise SystemExit("❌ alpha violates upper theoretical bound")

if upper > 5.0:
    raise SystemExit("❌ theoretical upper bound exceeds physical stability region")

print("✅ THEORETICAL CONSISTENCY HOLDS")
