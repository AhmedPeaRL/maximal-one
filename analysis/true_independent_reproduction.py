import subprocess
import tempfile
import os
import hashlib
import json
import time

REPO_URL = "https://github.com/ahmedpearl/maximal-one.git"


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


def run_fresh_clone():
    tmp = tempfile.mkdtemp()

    print("Cloning fresh repo...")

    subprocess.run([
        "git", "clone",
        "--filter=blob:none",
        REPO_URL,
        tmp
    ], check=True)

    return tmp


def run_pipeline(path):
    print("Running independent pipeline...")

    env = os.environ.copy()

    env.update({
        "PYTHONHASHSEED": "0",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1"
    })

    subprocess.run(
        ["python", "scripts/generate_report.py", "--seed", "42", "--canonical"],
        cwd=path,
        check=True,
        env=env
    )

    report_path = os.path.join(path, "artifacts", "canonical_report.json")

    if not os.path.exists(report_path):
        raise Exception("Missing report")

    with open(report_path) as f:
        return f.read()


def normalize(raw):
    data = json.loads(raw)

    def clean(obj):
        if isinstance(obj, dict):
            return {
                k: clean(v)
                for k, v in obj.items()
                if k not in ["timestamp", "_environment", "_sealed"]
            }

        if isinstance(obj, list):
            return [clean(x) for x in obj]

        if isinstance(obj, float):
            # 🔥 تثبيت أقوى
            return float(format(obj, ".6f"))

        return obj

    cleaned = clean(data)

    return json.dumps(
        cleaned,
        sort_keys=True,
        separators=(',', ':')
    )

    assert "spectral_profile" in cleaned
    assert "estimated_alpha" in cleaned["spectral_profile"]
    
   
def compare():
    local_path = "artifacts/canonical_report.json"

    with open(local_path) as f:
        local_raw = f.read()

    local_norm = normalize(local_raw)
    local_data = json.loads(local_norm)

    external_repo = run_fresh_clone()

    subprocess.run(
        ["git", "checkout", os.environ.get("GITHUB_SHA", "HEAD")],
        cwd=external_repo,
        check=True
    )

    external_raw = run_pipeline(external_repo)
    external_norm = normalize(external_raw)
    external_data = json.loads(external_norm)

    print("🔍 Comparing semantic structure...")

    def extract_key_metrics(data):
        return {
            "alpha": data["spectral_profile"]["estimated_alpha"],
            "std": data["spectral_profile"]["bootstrap_std"],
            "p": data["statistical_test"]["p_value"]
        }

    local_metrics = extract_key_metrics(local_data)
    external_metrics = extract_key_metrics(external_data)

    print("LOCAL:", local_metrics)
    print("EXTERNAL:", external_metrics)

    def close(a, b, tol):
        return abs(a - b) < tol

    if (
        close(local_metrics["alpha"], external_metrics["alpha"], 0.05) and
        close(local_metrics["std"], external_metrics["std"], 0.05) and
        close(local_metrics["p"], external_metrics["p"], 0.02)
    ):
        print("✅ SEMANTIC REPRODUCTION CONFIRMED")
        return True

    print("❌ SEMANTIC DIVERGENCE DETECTED")
    return False


if __name__ == "__main__":
    ok = compare()
    if not ok:
        exit(1)
