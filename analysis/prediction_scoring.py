import json
import os

ART = "artifacts"

def load(name):
    p = os.path.join(ART, name)
    if os.path.exists(p):
        return json.load(open(p))
    return None

pred = load("pre_registration.json")
report = load("canonical_report.json")

score = 0.0

if pred and report:
    alpha = report["spectral_profile"]["estimated_alpha"]
    lo, hi = pred["expected_alpha_range"]

    if lo <= alpha <= hi:
        score += 0.5

    # simple structure match
    if "periodic" in pred["expected_structure"]:
        if report["spectral_profile"]["estimated_alpha"] > 0.5:
            score += 0.3

result = {
    "prediction_score": score,
    "passed": score >= 0.5
}

with open(os.path.join(ART, "prediction_score.json"), "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
