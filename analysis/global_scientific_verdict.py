import json
import pathlib

ART = pathlib.Path("artifacts")


def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None


# -----------------------------
# Load signals
# -----------------------------

lorenz = load("lorenz.json")
lorenz96 = load("lorenz96.json")
bench = load("chaotic_benchmark.json")

temporal = load("temporal_dominance.json")
universality = load("universality_gate.json")
universality_stability = load("universality_stability.json")


# -----------------------------
# HARD REALITY CHECK
# -----------------------------

def predictive_success(d):
    if not d or d.get("skipped", False):
        return None
    return d.get("hcm_superior", False)


predictive_results = [
    predictive_success(lorenz),
    predictive_success(lorenz96),
    predictive_success(bench)
]

valid = [r for r in predictive_results if r is not None]

real_pass_ratio = sum(valid) / len(valid) if valid else 0.0


# 🔥 HARD GATE: لا نجاح بدون تفوق حقيقي
HARD_THRESHOLD = 0.5
predictive_pass = real_pass_ratio >= HARD_THRESHOLD


# -----------------------------
# Temporal signal
# -----------------------------

temporal_boost = 0.0

if temporal:
    if temporal.get("temporal_signal"):
        temporal_boost = 0.2


# -----------------------------
# Universality
# -----------------------------

universality_passed = universality and universality.get("passed", False)
universality_stable = universality_stability and universality_stability.get("passed", False)


# -----------------------------
# FINAL SCORE (بعد التصحيح)
# -----------------------------

score = 0.0

# 🚨 predictive is dominant now
score += real_pass_ratio * 0.7

if universality_passed:
    score += 0.15

if universality_stable:
    score += 0.1

score += temporal_boost


# -----------------------------
# FINAL DECISION
# -----------------------------

result = {
    "predictive_pass_ratio": real_pass_ratio,
    "predictive_pass": predictive_pass,
    "temporal_boost": temporal_boost,
    "universality_passed": universality_passed,
    "universality_stable": universality_stable,
    "final_score": score,
    "passed": predictive_pass and score >= 0.6,
    "confidence_level": (
        "strong" if score > 0.8 else
        "moderate" if score > 0.6 else
        "weak"
    )
}

ART.mkdir(exist_ok=True)
(ART / "global_verdict.json").write_text(json.dumps(result, indent=2))

print(json.dumps(result, indent=2))
