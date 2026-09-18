import json
import os

OUTPUT = "artifacts/universality_gate.json"

def safe_load(path):
    if not os.path.exists(path):
        return None

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def finite_number(value):
    try:
        value = float(value)
        return value if value == value else None
    except Exception:
        return None

inv = safe_load(
    "artifacts/universal_invariant_test.json"
)

signal = safe_load(
    "artifacts/global_signal.json"
)

components = {}
missing = []

if inv and "score" in inv:
    value = finite_number(inv["score"])

    if value is not None:
        components["universal_invariant"] = value
    else:
        missing.append("universal_invariant")

else:
    missing.append("universal_invariant")

if signal and "strength" in signal:
    value = finite_number(signal["strength"])

    if value is not None:
        components["global_signal"] = value
    else:
        missing.append("global_signal")

else:
    missing.append("global_signal")

os.makedirs("artifacts", exist_ok=True)

if not components:
    result = {
        "status": "not_evaluable",
        "passed": False,
        "scientific_claim": False,
        "reason": "No valid universality inputs",
        "missing_inputs": missing
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

    # Soft layer: absence of evidence is recorded,
    # but it is not mislabeled as model falsification.
    raise SystemExit(2)

weights = {
    "universal_invariant": 0.6,
    "global_signal": 0.4
}

weighted_sum = 0.0
weight_sum = 0.0

for name, value in components.items():
    weight = weights[name]
    weighted_sum += weight * value
    weight_sum += weight

raw_score = weighted_sum / weight_sum

result = {
    "status": "evaluated",
    "scientific_claim": False,
    "raw_weighted_score": float(raw_score),
    "components": components,
    "missing_inputs": missing,
    "method": "weighted_diagnostic_summary",
    "nonlinear_score_mapping": False,
    "passed": False,
    "interpretation": (
        "Diagnostic only. "
        "This score does not establish universality."
    )
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
raise SystemExit(0)
