import json
import os
import time
import hashlib

CHALLENGE_FILE = "data/external_challenges.json"
RESPONSES_FILE = "data/challenge_responses.json"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def hash_entry(entry):
    return hashlib.sha256(
        json.dumps(entry, sort_keys=True).encode()
    ).hexdigest()

def process_challenges():
    challenges = load_json(CHALLENGE_FILE, [])
    responses = load_json(RESPONSES_FILE, [])

    existing_ids = {r["challenge_id"] for r in responses}

    for c in challenges:
        cid = c.get("id")

        if cid in existing_ids:
            continue

        # simple evaluation layer (replace later with real engine)
        result = {
            "challenge_id": cid,
            "timestamp": time.time(),
            "status": "processed",
            "verdict": evaluate(c),
        }

        result["hash"] = hash_entry(result)

        responses.append(result)

    save_json(RESPONSES_FILE, responses)

def evaluate(challenge):
    text = challenge.get("challenge", "")

    if len(text) < 5:
        return "rejected: too weak"

    if "prove" in text.lower():
        return "accepted: routed to scientific validation"

    return "recorded: awaiting escalation"

if __name__ == "__main__":
    process_challenges()
