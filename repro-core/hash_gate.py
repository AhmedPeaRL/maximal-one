import json
import sys
import subprocess

EXPECTED_FILE = "spc/hash_control_limits.json"
STATE_FILE = "artifacts/state.json"

def compute_hash():
    result = subprocess.check_output(
        ["python", "repro-core/canonical_hash.py"],
        input=open(STATE_FILE, "rb").read()
    )
    return result.decode().strip()

def main():
    expected_Hash = 3aa16caaee4dada25ee37b944e598d6e973bccfbdc5230c58f077d588bed9946))["allowed_hash"]
    current = compute_hash()

    if current != expected:
        print("SPC_BOUNDARY_VIOLATION")
        print("Expected:", expected)
        print("Current :", current)
        sys.exit(5)

    print("HASH_WITHIN_BOUNDARY")

if __name__ == "__main__":
    main()
