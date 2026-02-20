#!/usr/bin/env python3

import json
from pathlib import Path
import sys
from datetime import datetime

LOG_FILE = Path("state/state-transitions.json")

def load():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []

def save(data):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(json.dumps(data, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    state = sys.argv[1]
    history = load()

    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "state": state
    })

    save(history)
