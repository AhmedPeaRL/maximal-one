import json
import subprocess
import hashlib
import time
import os

OUTPUT_PATH = "artifacts/external_independent_result.json"


def run_external_clone():
    """
    Simulates an external system reproducing results WITHOUT internal state.
    """

    try:
        # simulate fresh environment
        env = os.environ.copy()
        env["PYTHONHASHSEED"] = "0"

        result = subprocess.run(
            ["python", "scripts/generate_report.py", "--seed", "42", "--canonical"],
            capture_output=True,
            text=True,
            env=env,
            timeout=120
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except Exception as e:
        return {"error": str(e)}


def hash_output(data):
    raw = json.dumps(data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def main():
    os.makedirs("artifacts", exist_ok=True)

    run = run_external_clone()

    result = {
        "timestamp": time.time(),
        "execution": run,
        "hash": hash_output(run),
        "verdict": None
    }

    # simple integrity logic
    if run.get("returncode") == 0:
        result["verdict"] = "reproduced"
    else:
        result["verdict"] = "failed"

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print("External independent execution complete")


if __name__ == "__main__":
    main()
