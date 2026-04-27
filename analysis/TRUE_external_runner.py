import subprocess
import tempfile
import shutil
import os
import json
import hashlib

REPO = "https://github.com/AhmedPeaRL/maximal-one.git"

def run_external():
    tmp = tempfile.mkdtemp()

    try:
        os.chdir(tmp)

        # Clone fresh (no history bias)
        subprocess.run(["git", "clone", "--depth=1", REPO, "repo"], check=True)

        os.chdir("repo")

        # Install fresh environment
        subprocess.run(["pip", "install", "--no-cache-dir", "-r", "requirements-lock.txt"], check=True)

        # Run core experiment
        subprocess.run(["python", "scripts/generate_report.py", "--seed", "42", "--canonical"], check=True)

        # Load result
        with open("artifacts/canonical_report.json") as f:
            report = json.load(f)

        alpha = report["spectral_profile"]["estimated_alpha"]

        # Independent hash
        h = hashlib.sha256(json.dumps(report, sort_keys=True).encode()).hexdigest()

        print("EXTERNAL ALPHA:", alpha)
        print("EXTERNAL HASH:", h)

        if alpha is None:
            raise Exception("Invalid alpha")

        print("✅ TRUE EXTERNAL RUN SUCCESS")

    finally:
        shutil.rmtree(tmp)

if __name__ == "__main__":
    run_external()
