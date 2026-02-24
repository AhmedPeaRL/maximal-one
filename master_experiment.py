import numpy as np
import platform
import hashlib
import json
import subprocess
import time

from core.environment_fingerprint import generate_environment_fingerprint
from core.positive_control import power_curve_test
from core.spectral_experiment import run_spectral_test
from core.theoretical_guard import validate_environment


def environment_fingerprint_local():
    env = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "uname": platform.uname()._asdict(),
    }

    try:
        node_version = subprocess.check_output(
            ["node", "--version"]
        ).decode().strip()
    except Exception:
        node_version = None

    env["node_version"] = node_version

    raw = json.dumps(env, sort_keys=True).encode()
    env_hash = hashlib.sha256(raw).hexdigest()

    return env, env_hash


def write_environment_files():
    env, env_hash = environment_fingerprint_local()

    with open("environment.json", "w") as f:
        json.dump(env, f, indent=2)

    with open("hash.txt", "w") as f:
        f.write(env_hash)

    return env_hash


def run_experiment(seed=None):
    if seed is not None:
        np.random.seed(seed)

    data = np.random.normal(loc=0.0, scale=1.0, size=1000)

    mean = float(np.mean(data))
    std = float(np.std(data))
    z_score = float(mean / (std / np.sqrt(len(data))))

    return {
        "mean": mean,
        "std": std,
        "max_zscore": abs(z_score),
        "significant": abs(z_score) > 3.0
    }


def main():
    validate_environment()

    write_environment_files()

    np.random.seed(42)
    baseline = np.random.normal(0, 1, 2048)

    env_hash = generate_environment_fingerprint()
    print(f"Environment hash (external module): {env_hash}")

    result = run_spectral_test(baseline, alpha=0.01)

    report = {
        "timestamp": time.time(),
        "max_zscore": result["max_zscore"],
        "empirical_threshold": result["empirical_threshold"],
        "significant": result["significant"],
        "sample_size": len(baseline),
        "null_hypothesis": "No intrinsic periodic structure"
    }

    with open("state.json", "w") as f:
        json.dump(report, f, indent=2)

    print(report)


if __name__ == "__main__":
    main()
