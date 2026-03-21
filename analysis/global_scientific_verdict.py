import json
import pathlib

ART = pathlib.Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

def score_signal(d):
    if not d:
        return None

    if d.get("skipped", False):
        return None

    base = 1.0 if d.get("hcm_superior", False) else 0.0
    confidence = d.get("confidence", 0.5)

    return base * confidence


lorenz = load("lorenz.json")
lorenz96 = load("lorenz96.json")
bench = load("chaotic_benchmark.json")

raw_scores = [
    score_signal(lorenz),
    score_signal(lorenz96),
    score_signal(bench)
]

# استبعاد skipped فقط
scores = [s for s in raw_scores if s is not None]

total = sum(scores)
n = len(scores)

temporal = load("temporal_dominance.json")

temporal_boost = 0.0

if temporal:
    strength = temporal.get("signal_strength", 0.0)

    if temporal.get("temporal_signal"):
        temporal_boost = 0.4
    else:
        temporal_boost = min(0.2, strength * 0.01)

ratio = (total / n if n > 0 else 0) + temporal_boost

result = {
    "tests_run": n,
    "score_sum": total,
    "score_ratio": ratio,
    "global_superiority": ratio > 0.55,
    "confidence_level": (
        "strong" if ratio > 0.75 else
        "moderate" if ratio > 0.55 else
        "weak"
    )
}

(ART/"global_verdict.json").write_text(json.dumps(result, indent=2))

print(result)
