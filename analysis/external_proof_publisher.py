import json
import hashlib
import time

def main():
    with open("public/repro_bundle/canonical_report.json") as f:
        report = json.load(f)

    raw = json.dumps(report, sort_keys=True).encode()
    h = hashlib.sha256(raw).hexdigest()

    proof = {
        "hash": h,
        "timestamp": time.time()
    }

    with open("public/external_proof.json", "w") as f:
        json.dump(proof, f, indent=2)

    print("External proof generated")

if __name__ == "__main__":
    main()
