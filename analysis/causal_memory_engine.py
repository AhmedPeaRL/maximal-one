import json
import os
import time
import hashlib

MEMORY_PATH = "data/causal_memory.json"


def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH) as f:
        return json.load(f)


def save_memory(memory):
    os.makedirs("data", exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)


def hash_event(event):
    raw = json.dumps(event, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def record_event(decision, score, layer, context=None):
    memory = load_memory()

    event = {
        "timestamp": time.time(),
        "decision": decision,
        "score": score,
        "layer": layer,
        "context": context or {}
    }

    event["hash"] = hash_event(event)

    memory.append(event)

    # keep only last 500 events (bounded memory)
    memory = memory[-500:]

    save_memory(memory)

    print("Event recorded:", event["hash"])


def analyze_memory():
    memory = load_memory()

    if not memory:
        return {"status": "empty"}

    scores = [e["score"] for e in memory if "score" in e]

    avg_score = sum(scores) / len(scores) if scores else 0

    drift = scores[-1] - scores[0] if len(scores) > 1 else 0

    return {
        "events": len(memory),
        "avg_score": avg_score,
        "drift": drift,
        "last_layer": memory[-1]["layer"]
    }


if __name__ == "__main__":
    stats = analyze_memory()
    print(json.dumps(stats, indent=2))
