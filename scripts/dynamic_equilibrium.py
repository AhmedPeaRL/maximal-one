#!/usr/bin/env python3

import json
from pathlib import Path

STATE_FILE = Path("state/statistical-state.json")

CV_THRESHOLD = 0.02

if STATE_FILE.exists():
    state = json.loads(STATE_FILE.read_text())
    cv = state.get("cv", 0.0)

    if cv < CV_THRESHOLD:
        print("EQUILIBRIUM=stable")
    else:
        print("EQUILIBRIUM=unstable")
else:
    print("NO_STATE")
