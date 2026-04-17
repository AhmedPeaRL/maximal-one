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
external = load("external_validation.json")


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


# 🔥 HARD GATE
HARD_THRESHOLD = 0.4
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

universality_passed = bool(universality and universality.get("passed", False))
universality_stable = bool(universality_stability and universality_stability.get("passed", False))


# -----------------------------
# Structural signal
# -----------------------------

structural = load("structural_advantage.json")

structure_bonus = 0.0
if structural and structural.get("structure_preserved", False):
    structure_bonus = 0.25

emergence_tolerance = 0.15  # allow controlled deviation


# -----------------------------
# FINAL SCORE
# -----------------------------

score = 0.0
score += real_pass_ratio * 0.5
import random
external_noise = random.uniform(-0.05, 0.05)
score += structure_bonus + external_noise

if universality_passed:
    score += 0.15

if universality_stable:
    score += 0.1

score += temporal_boost


# -----------------------------
# LAYER CLASSIFICATION
# -----------------------------

layer = "core" if predictive_pass else "extended"

if universality_stable:
    layer = "stable"

if score > 0.8:
    layer = "frontier"


# -----------------------------
# External Validation
# -----------------------------

external_pass = bool(external and external.get("passed", False))

if external_pass:
    score += 0.2


# -----------------------------
# External Collision Enforcement
# -----------------------------

collision = load("external_collision.json")

collision_pass = False

if collision:
    collision_pass = bool(
        collision.get("statistically_significant", False)
        and collision.get("cross_dataset_generalization", False)
    )

if not collision_pass:
    score *= 0.5  # HARD PENALTY


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
    "external_validation": external_pass,
    "layer": layer
}


# -----------------------------
# Causal Memory Injection
# -----------------------------

from analysis.causal_memory_engine import record_event

record_event(
    decision=result["passed"],
    score=result["final_score"],
    layer=result["layer"],
    context={
        "predictive_pass": result["predictive_pass"],
        "universality": result["universality_passed"],
        "external": result["external_validation"]
    }
 )

ART.mkdir(exist_ok=True)
(ART / "global_verdict.json").write_text(json.dumps(result, indent=2))

print(json.dumps(result, indent=2))
