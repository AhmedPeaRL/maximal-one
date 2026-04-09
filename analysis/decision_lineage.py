import json, os, hashlib, datetime

BASE = "data/decision_lineage.json"

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
