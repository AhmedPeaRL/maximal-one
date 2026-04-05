import json
from pathlib import Path

history_path = Path("data/claim_history.json")
current_path = Path("artifacts/claim_verification.json")

if not current_path.exists():
    raise RuntimeError("Missing claim verification result")

current = json.load(open(current_path))

if history_path.exists():
    history = json.load(open(history_path))
else:
    history = []

history.append(current)

Path("data").mkdir(exist_ok=True)
with open(history_path, "w") as f:
    json.dump(history, f, indent=2)

print(f"History length: {len(history)}")
