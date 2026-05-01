import json
import os

OUTPUT = "artifacts/universality_gate.json"

def safe_load(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)

inv = safe_load("artifacts/universal_invariant_test.json")
signal = safe_load("artifacts/global_signal.json")

components = []

if inv and "score" in inv:
    components.append(0.6 * float(inv["score"]))

if signal and "strength" in signal:
    components.append(0.4 * float(signal["strength"]))

if len(components) == 0:
    raise SystemExit("❌ No valid inputs for universality gate")

score = sum(components)

threshold = 0.55

result = {
    "score": score,
    "threshold": threshold,
    "passed": score > threshold,
    "components": components
}

os.makedirs("artifacts", exist_ok=True)

with open(OUTPUT, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
