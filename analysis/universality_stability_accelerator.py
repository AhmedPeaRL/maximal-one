import json
import pathlib

ART = pathlib.Path("artifacts")
DATA = pathlib.Path("data")

gate_file = ART / "universality_gate.json"
history_file = DATA / "universality_history.json"

def safe_float(x):
    try:
        return float(x)
    except:
        return None

if not gate_file.exists():
    print("No universality gate found")
    exit()

current = json.loads(gate_file.read_text())

if not history_file.exists():
    history = []
else:
    try:
        history = json.loads(history_file.read_text())
    except:
        history = []

# 🔥 تنظيف التاريخ بالكامل (hard sanitization)
clean_history = []
for x in history:
    if isinstance(x, dict):
        continue
    v = safe_float(x)
    if v is not None:
        clean_history.append(v)

history = clean_history

strength = safe_float(current.get("strength", 0.0))
if strength is None:
    strength = 0.0

# 🧠 intelligent persistence
if len(history) > 0:
    last = history[-1]

    if abs(strength - last) < 0.02:
        blended = (strength + last) / 2
        history.append(blended)
    else:
        history.append(strength)
else:
    history.append(strength)

# keep bounded history
history = history[-20:]

history_file.parent.mkdir(parents=True, exist_ok=True)
history_file.write_text(json.dumps(history, indent=2))

print({
    "status": "accelerated_clean",
    "new_length": len(history),
    "last_value": history[-1]
})
