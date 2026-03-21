import json
import pathlib

ART = pathlib.Path("artifacts")
DATA = pathlib.Path("data")

gate_file = ART / "universality_gate.json"
history_file = DATA / "universality_history.json"

if not gate_file.exists():
    print("No universality gate found")
    exit()

current = json.loads(gate_file.read_text())

if not history_file.exists():
    history = []
else:
    history = json.loads(history_file.read_text())

strength = float(current.get("strength", 0.0))

# 🧠 intelligent persistence (not blind duplication)
if len(history) > 0:
    last = history[-1]

    # if signal is stable → reinforce slightly
    if abs(strength - last) < 0.02:
        blended = (strength + last) / 2
        history.append(blended)
    else:
        history.append(strength)
else:
    history.append(strength)

# keep bounded history
history = history[-20:]

history_file.write_text(json.dumps(history, indent=2))

print({
    "status": "accelerated",
    "new_length": len(history),
    "last_value": history[-1]
})
