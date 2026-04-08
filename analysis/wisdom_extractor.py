import json
import os
from collections import Counter

DATA_PATH = "data"

def load_events():
    events = []
    for root, _, files in os.walk(DATA_PATH):
        for f in files:
            if f.endswith(".json"):
                try:
                    with open(os.path.join(root, f)) as file:
                        events.append(json.load(file))
                except:
                    pass
    return events

def extract_patterns(events):
    keys = []
    for e in events:
        if isinstance(e, dict):
            keys.extend(e.keys())

    return Counter(keys).most_common(10)

def build_wisdom():
    events = load_events()
    patterns = extract_patterns(events)

    return {
        "total_events": len(events),
        "dominant_patterns": patterns
    }

if __name__ == "__main__":
    wisdom = build_wisdom()
    print(json.dumps(wisdom, indent=2))
