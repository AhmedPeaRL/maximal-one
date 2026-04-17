import json, os, sys

CURRENT_PATH = "artifacts/canonical_report.json"
HISTORY_PATH = "artifacts/alpha_history.json"

if not os.path.exists(CURRENT_PATH):
    print("Missing report")
    sys.exit(1)

with open(CURRENT_PATH) as f:
    current = json.load(f)

alpha = current["spectral_profile"]["estimated_alpha"]

history = []

if os.path.exists(HISTORY_PATH):
    with open(HISTORY_PATH) as f:
        history = json.load(f)

history.append(alpha)

# keep last 10
history = history[-10:]

# compute drift
if len(history) > 2:
    diffs = [abs(history[i] - history[i-1]) for i in range(1,len(history))]
    drift = sum(diffs)/len(diffs)

    if drift > 0.05:
        print("⚠️ Alpha drift too high:", drift)
        sys.exit(1)

with open(HISTORY_PATH,"w") as f:
    json.dump(history,f,indent=2)

print("Alpha continuity stable.")
