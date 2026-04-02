import json
from pathlib import Path
import sys

path = Path("artifacts/anti_triviality_hard.json")

if not path.exists():
    print("Anti-triviality result missing → FAIL")
    sys.exit(1)

data = json.loads(path.read_text())

CRITICAL_TESTS = ["original", "nonlinear"]

failures = []

for key, val in data.items():

    if key not in CRITICAL_TESTS:
        continue

    if isinstance(val, dict):

        if val.get("skipped", False):
            continue

        if not val.get("hcm_better", False):
            failures.append(key)

if failures:
    print("HCM failed critical anti-triviality on:", failures)
    sys.exit(1)

print("HCM passed critical anti-triviality gate")
