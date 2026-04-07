import json
import os
import hashlib
from datetime import datetime

CHAIN_FILE = "data/witness_chain.json"

def load_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE) as f:
        return json.load(f)

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def append_witness(payload):
    chain = load_chain()

    prev_hash = chain[-1]["hash"] if chain else "genesis"

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload,
        "prev_hash": prev_hash
    }

    raw = json.dumps(entry, sort_keys=True).encode()
    entry["hash"] = hashlib.sha256(raw).hexdigest()

    chain.append(entry)
    save_chain(chain)

if __name__ == "__main__":
    import sys
    payload = json.loads(sys.argv[1])
    append_witness(payload)
