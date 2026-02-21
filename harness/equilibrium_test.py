#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np

STATE = Path("state/history.json")

if not STATE.exists():
    print("NO_HISTORY")
    exit()

history = json.loads(STATE.read_text())
cvs = [h["cv"] for h in history if "cv" in h]

if len(cvs) < 5:
    print("INSUFFICIENT_DATA")
    exit()

if np.std(cvs[-10:]) < 0.01:
    print("DYNAMIC_EQUILIBRIUM=stable")
else:
    print("DYNAMIC_EQUILIBRIUM=unstable")
