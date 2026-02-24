import hashlib
import json
import os
import platform
import subprocess
import sys


def get_cpu_flags():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("flags"):
                    return line.strip()
    except Exception:
        return "cpu_flags_unavailable"
    return "cpu_flags_missing"


def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except Exception:
        return "cmd_failed"


def collect_environment():
    data = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "uname": run_cmd("uname -a"),
        "lsb_release": run_cmd("lsb_release -a"),
        "pip_freeze": run_cmd("pip freeze"),
        "cpu_flags": get_cpu_flags(),
    }
    return data


def compute_hash(data):
    blob = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


if __name__ == "__main__":
    env_data = collect_environment()
    env_hash = compute_hash(env_data)

    os.makedirs("env", exist_ok=True)

    with open("env/environment.json", "w") as f:
        json.dump(env_data, f, indent=2)

    with open("env/environment_hash.txt", "w") as f:
        f.write(env_hash)

    print("Environment hash:", env_hash)
