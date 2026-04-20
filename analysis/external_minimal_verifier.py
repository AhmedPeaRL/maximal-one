import json
import hashlib
import subprocess
import sys

def sha256_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def run():
    print("=== EXTERNAL VERIFIER START ===")

    try:
        subprocess.run(
            ["python", "scripts/generate_report.py", "--seed", "42", "--canonical"],
            check=True
        )
    except Exception as e:
        print("Execution failed:", e)
        sys.exit(1)

    new_hash = sha256_file("artifacts/canonical_report.json")

    with open("artifacts/report.hash") as f:
        expected_hash = f.read().strip()

    print("Expected:", expected_hash)
    print("Actual:", new_hash)

    if new_hash != expected_hash:
        print("❌ HASH MISMATCH → INVALID SYSTEM")
        sys.exit(1)

    with open("artifacts/canonical_report.json") as f:
        r = json.load(f)

    alpha = r["spectral_profile"]["estimated_alpha"]
    sigma = r["spectral_profile"]["bootstrap_std"]

    print("Alpha:", alpha)
    print("Sigma:", sigma)

    if sigma > 0.2:
        print("❌ HIGH UNCERTAINTY")
        sys.exit(1)

    print("✅ EXTERNAL VERIFICATION PASSED")

if __name__ == "__main__":
    run()
