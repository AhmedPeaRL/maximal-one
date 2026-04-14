import json
import time
import hashlib
import os

from arweave import Wallet, Transaction

ARTIFACT_PATH = "artifacts/canonical_report.json"
OUTPUT_LOG = "data/arweave_anchor_log.json"
KEY_PATH = "secrets/arweave-key.json"


def compute_hash():
    if not os.path.exists(ARTIFACT_PATH):
        return None

    with open(ARTIFACT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_wallet():
    if not os.path.exists(KEY_PATH):
        raise Exception("Missing Arweave key")

    return Wallet(KEY_PATH)


def send_to_arweave(wallet, payload):
    data = json.dumps(payload).encode()

    tx = Transaction(wallet, data=data)
    tx.add_tag("App-Name", "maximal-one")
    tx.add_tag("Type", "scientific-anchor")
    tx.add_tag("Content-Type", "application/json")

    tx.sign()
    tx.send()

    return tx.id


def store_local(hash_value, tx_id):
    os.makedirs("data", exist_ok=True)

    entry = {
        "timestamp": time.time(),
        "hash": hash_value,
        "tx_id": tx_id
    }

    if os.path.exists(OUTPUT_LOG):
        with open(OUTPUT_LOG) as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(OUTPUT_LOG, "w") as f:
        json.dump(data, f, indent=2)


def main():
    h = compute_hash()

    if not h:
        print("No artifact found")
        return

    wallet = load_wallet()

    payload = {
        "hash": h,
        "timestamp": time.time(),
        "source": "maximal-one"
    }

    tx_id = send_to_arweave(wallet, payload)

    store_local(h, tx_id)

    print("ARWEAVE TX:", tx_id)


if __name__ == "__main__":
    main()
