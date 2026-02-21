#!/usr/bin/env python3
import json
from pathlib import Path

STATE = Path("state/statistical-state.json")

if not STATE.exists():
    exit(0)

data = json.loads(STATE.read_text())
variance = data.get("variance", 0.0)

V = variance

print(f"V={V}")
