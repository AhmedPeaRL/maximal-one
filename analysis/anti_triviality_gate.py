import json
from pathlib import Path
import sys

path = Path("artifacts/anti_triviality_hard.json")

if not path.exists():
    print("Anti-triviality result missing → FAIL")
    sys.exit(1)

data = json.loads(path.read_text())

failures = []

for key, val in data.items():

    if isinstance(val, dict):

        # 🔥 skip trivial cases
        if val.get("skipped", False):
            continue

        if not val.get("hcm_better", False):
            failures.append(key)

if failures:
    print("HCM failed anti-triviality on:", failures)
    sys.exit(1)

print("HCM passed anti-triviality gate")
