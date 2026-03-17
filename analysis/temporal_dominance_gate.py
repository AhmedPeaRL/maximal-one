import json
import pathlib

ART = pathlib.Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None

long_run = load("long_run_results.json") or load("long_run.json")

result = {
    "temporal_signal": False,
    "improvement": 0.0,
    "p_value": 1.0,
    "significant": False
}

if long_run:
    improvement = long_run.get("improvement", 0.0)
    p = long_run.get("p_value", 1.0)

    result["improvement"] = improvement
    result["p_value"] = p

    # الشرط الحقيقي
    if improvement > 0.01 and p < 1e-5:
        result["temporal_signal"] = True
        result["significant"] = True

(ART / "temporal_dominance.json").write_text(json.dumps(result, indent=2))
print(result)
