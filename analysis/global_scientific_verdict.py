import json
import pathlib
import sys

ART = pathlib.Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None


# -----------------------------
# Load all signals
# -----------------------------

lorenz = load("lorenz.json")
lorenz96 = load("lorenz96.json")
bench = load("chaotic_benchmark.json")
temporal = load("temporal_dominance.json")
universality = load("universality_gate.json")
universality_stability = load("universality_stability.json")
topology = load("topology.json")  # optional


# -----------------------------
# Signal scoring
# -----------------------------

def score_signal(d):
    if not d:
        return None

    if d.get("skipped", False):
        return None

    base = 1.0 if d.get("hcm_superior", False) else 0.0
    confidence = d.get("confidence", 0.5)

    return base * confidence


raw_scores = [
    score_signal(lorenz),
    score_signal(lorenz96),
    score_signal(bench)
]

scores = [s for s in raw_scores if s is not None]

total = sum(scores)
n = len(scores)


# -----------------------------
# Temporal boost
# -----------------------------

temporal_boost = 0.0

if temporal:
    strength = temporal.get("signal_strength", 0.0)

    if temporal.get("temporal_signal"):
        temporal_boost = 0.5
    else:
        temporal_boost = min(0.2, strength * 0.01)


# -----------------------------
# Universality
# -----------------------------

universality_passed = False
if universality:
    universality_passed = universality.get("passed", False)

universality_stable = False
if universality_stability:
    universality_stable = universality_stability.get("passed", False)


# -----------------------------
# Topology (optional soft signal)
# -----------------------------

topology_ok = False
if topology:
    topology_ok = topology.get("passed", False)


# -----------------------------
# Final scoring logic (clean)
# -----------------------------

ratio = (total / n if n > 0 else 0) + temporal_boost

score = 0.0

# base predictive evidence
if ratio > 0.55:
    score += 0.4

if ratio > 0.65:
    score += 0.1

# universality
if universality_passed:
    score += 0.2

# stability
if universality_stable:
    score += 0.15

# topology (soft)
if topology_ok:
    score += 0.05


# -----------------------------
# Final result
# -----------------------------

result = {
    "tests_run": n,
    "score_sum": total,
    "score_ratio": ratio,
    "temporal_boost": temporal_boost,
    "global_superiority": ratio > 0.55,
    "confidence_level": (
        "strong" if ratio > 0.75 else
        "moderate" if ratio > 0.55 else
        "weak"
    ),
    "final_score": score,
    "passed": score >= 0.65
}

ART.mkdir(exist_ok=True)
(ART / "global_verdict.json").write_text(json.dumps(result, indent=2))

print(json.dumps(result, indent=2))
