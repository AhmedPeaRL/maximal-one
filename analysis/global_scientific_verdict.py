import json
import pathlib
import math

ART = pathlib.Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

def score_signal(d):
    if not d:
        return 0.0

    base = 1.0 if d.get("hcm_superior", False) else 0.0

    # soft confidence boost لو فيه structure
    confidence = d.get("confidence", 0.5)
    return base * confidence

lorenz = load("lorenz.json")
lorenz96 = load("lorenz96.json")
bench = load("chaotic_benchmark.json")

scores = [
    score_signal(lorenz),
    score_signal(lorenz96),
    score_signal(bench)
]

scores = [s for s in scores if s is not None]

total = sum(scores)
n = len(scores)

temporal = load("temporal_dominance.json")

temporal_boost = 0.0
if temporal and temporal.get("temporal_signal"):
    temporal_boost = 0.4   # boost تقيل لأنه أقوى دليل

# continuous superiority بدل binary
ratio = (total / n if n > 0 else 0) + temporal_boost

result = {
    "tests_run": n,
    "score_sum": total,
    "score_ratio": ratio,
    "global_superiority": ratio > 0.55,   # بدل 0.5 hard cut
    "confidence_level": (
        "strong" if ratio > 0.75 else
        "moderate" if ratio > 0.55 else
        "weak"
    )
}

(ART/"global_verdict.json").write_text(json.dumps(result, indent=2))

print(result)
