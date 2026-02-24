import sys
import subprocess
import hashlib
import platform
import json
import os
import datetime
import numpy as np

REPORT_DIR = "artifacts"
FREEZE_FILE = os.path.join(REPORT_DIR, "pip_freeze.txt")
REPORT_FILE = os.path.join(REPORT_DIR, "stability_report.json")

os.makedirs(REPORT_DIR, exist_ok=True)

def get_python_patch_version():
    return platform.python_version()

def get_platform_fingerprint():
    data = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_patch": get_python_patch_version(),
    }
    raw = json.dumps(data, sort_keys=True).encode()
    fingerprint = hashlib.sha256(raw).hexdigest()
    return data, fingerprint

def freeze_environment():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True
    )
    with open(FREEZE_FILE, "w") as f:
        f.write(result.stdout)
    return result.stdout

def nonlinear_stability_test():
    # اختبار بسيط لاخطي عبر logistic map
    r = 3.9
    x = 0.5
    values = []
    for _ in range(1000):
        x = r * x * (1 - x)
        values.append(x)
    arr = np.array(values)
    mean = float(np.mean(arr))
    std = float(np.std(arr))
    max_val = float(np.max(arr))
    min_val = float(np.min(arr))
    stable = std < 0.35  # معيار تحكمي قابل للتطوير
    return {
        "mean": mean,
        "std": std,
        "max": max_val,
        "min": min_val,
        "stable_under_threshold": stable
    }

def main():
    timestamp = datetime.datetime.utcnow().isoformat()

    platform_data, fingerprint = get_platform_fingerprint()
    freeze_output = freeze_environment()
    nonlinear_result = nonlinear_stability_test()

    report = {
        "timestamp_utc": timestamp,
        "environment": platform_data,
        "environment_fingerprint_sha256": fingerprint,
        "nonlinear_stability_test": nonlinear_result
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print("Report generated.")
    print("Environment fingerprint:", fingerprint)

if __name__ == "__main__":
    main()
