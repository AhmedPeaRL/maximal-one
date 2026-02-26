import json
import sys

MAX_BOUND = 10  # theoretical M

with open("artifacts/state.json") as f:
    state = json.load(f)

values = state.get("values", [])

for v in values:
    if abs(v) > MAX_BOUND:
        print("Bound violation detected")
        sys.exit(1)

print("Boundedness condition satisfied")
