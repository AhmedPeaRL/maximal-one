import json
import hashlib
import time
import os

CHALLENGE_LOG = "data/external_challenges.json"

def load_challenges():
    if not os.path.exists(CHALLENGE_LOG):
        return []
    with open(CHALLENGE_LOG) as f:
        return json.load(f)

def save_challenges(challenges):
    os.makedirs("data", exist_ok=True)
    with open(CHALLENGE_LOG, "w") as f:
        json.dump(challenges, f, indent=2)

def register_challenge(challenge_text):
    challenges = load_challenges()

    challenge_id = hashlib.sha256(
        (challenge_text + str(time.time())).encode()
    ).hexdigest()

    entry = {
        "id": challenge_id,
        "challenge": challenge_text,
        "timestamp": time.time(),
        "status": "pending",
        "response": None
    }

    challenges.append(entry)
    save_challenges(challenges)

    return challenge_id

def resolve_challenges():
    challenges = load_challenges()

    for c in challenges:
        if c["status"] != "pending":
            continue

        # VERY IMPORTANT: no interpretation
        # system must answer in measurable form only
        c["response"] = {
            "verdict": "not falsified",
            "confidence": 0.5,
            "note": "requires external replication"
        }

        c["status"] = "processed"

    save_challenges(challenges)

if __name__ == "__main__":
    resolve_challenges()
