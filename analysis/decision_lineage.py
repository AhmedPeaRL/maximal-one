import json, os, hashlib, datetime

BASE = "data/decision_lineage.json"

with open("core-scientific/decision_contract/decision_contract.json") as f:
    CONTRACT = json.load(f)

def load():
    if not os.path.exists(BASE):
        return []
    with open(BASE) as f:
        return json.load(f)

def save(data):
    with open(BASE, "w") as f:
        json.dump(data, f, indent=2)

def fingerprint(entry):
    return hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()

def enforce_decision(decision, signals):
    rules = CONTRACT["binding_rules"]

    if rules["reproducibility_required"] and not signals.get("reproducible"):
        return "rejected"

    if rules["falsifiability_required"] and not signals.get("falsifiable"):
        return "rejected"

    if rules["external_anchor_required"] and not signals.get("externally_anchored"):
        return "unstable"

    return decision
    
def append_decision(current_decision):
    lineage = load()

    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "decision": current_decision,
    }

    entry["fingerprint"] = fingerprint(entry)

    lineage.append(entry)

    save(lineage)

if __name__ == "__main__":
    with open("artifacts/decision.json") as f:
        decision = json.load(f)

    append_decision(decision)

    print("Decision lineage updated.")
