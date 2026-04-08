import json
import os

def load_hash(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return None

h18 = load_hash("node18/node_report.hash")
h20 = load_hash("node20/node_report.hash")
h24 = load_hash("node24/node_report.hash")

result = {
    "node18": h18,
    "node20": h20,
    "node24": h24,
    "consensus": (h18 == h20 == h24),
}

os.makedirs("artifacts", exist_ok=True)

with open("artifacts/runtime_divergence.json", "w") as f:
    json.dump(result, f, indent=2)

print("Runtime divergence observed:")
print(json.dumps(result, indent=2))
