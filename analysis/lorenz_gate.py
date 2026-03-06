import json
import sys
from pathlib import Path

path = Path("artifacts/lorenz96.json")

if not path.exists():
    print("missing_result")
    sys.exit(0)

try:
    data = json.loads(path.read_text())
except Exception:
    print("invalid_json")
    sys.exit(0)

improvement = float(data.get("improvement", 0))
p = float(data.get("p_value", 1))

passed = improvement > 0 and p < 0.05

print(json.dumps({
    "improvement": improvement,
    "p_value": p,
    "passed": passed
}))
