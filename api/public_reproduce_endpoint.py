import subprocess
import tempfile
import json
import os
import hashlib
import time

def run_external_reproduction(input_payload: dict):
    """
    ZERO-TRUST REPRODUCTION:
    Runs the system in a completely isolated temp environment.
    No dependency on internal state.
    """

    with tempfile.TemporaryDirectory() as tmp:

        # clone repo fresh
        subprocess.run([
            "git", "clone",
            "https://github.com/ahmedpearl/maximal-one.git",
            tmp
        ], check=True)

        # install dependencies
        subprocess.run([
            "pip", "install", "-r", "requirements-lock.txt"
        ], cwd=tmp, check=True)

        # write input
        payload_path = os.path.join(tmp, "external_input.json")
        with open(payload_path, "w") as f:
            json.dump(input_payload, f)

        # run core reproduction
        subprocess.run([
            "python",
            "analysis/external_reproduction.py",
            payload_path
        ], cwd=tmp, check=True)

        # read result
        result_path = os.path.join(tmp, "artifacts/reproduction_result.json")

        if not os.path.exists(result_path):
            return {"ok": False, "error": "no result"}

        with open(result_path) as f:
            result = json.load(f)

        # attach independent hash
        h = hashlib.sha256(
            json.dumps(result, sort_keys=True).encode()
        ).hexdigest()

        return {
            "ok": True,
            "result": result,
            "hash": h,
            "timestamp": time.time()
        }
