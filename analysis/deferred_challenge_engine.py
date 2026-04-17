import json
import os
import time

QUEUE = "data/deferred_challenges.json"

def load_queue():
    if not os.path.exists(QUEUE):
        return []
    return json.load(open(QUEUE))

def save_queue(q):
    os.makedirs("data", exist_ok=True)
    json.dump(q, open(QUEUE,"w"), indent=2)

def enqueue(challenge):
    q = load_queue()
    q.append({
        "challenge": challenge,
        "timestamp": time.time(),
        "status": "pending"
    })
    save_queue(q)

def process():
    q = load_queue()
    updated = []

    for item in q:
        if item["status"] == "pending":
            # simulate deferred evaluation
            item["status"] = "processed"
            item["resolution"] = "evaluated in future run"

        updated.append(item)

    save_queue(updated)

if __name__ == "__main__":
    process()
