import json
import pathlib

ART = pathlib.Path("artifacts")

scores = []

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

lorenz = load("lorenz.json")
lorenz96 = load("lorenz96.json")
bench = load("chaotic_benchmark.json")

if lorenz:
    scores.append(lorenz.get("hcm_superior",False))

if lorenz96:
    scores.append(lorenz96.get("hcm_superior",False))

if bench:
    scores.append(bench.get("hcm_superior",False))

result = {
    "tests_run": len(scores),
    "positive": sum(scores),
    "global_superiority": sum(scores) > len(scores)/2
}

(ART/"global_verdict.json").write_text(json.dumps(result,indent=2))

print(result)
