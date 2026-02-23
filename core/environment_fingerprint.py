import hashlib
import json
import os
import platform
import subprocess
import sys


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def get_dependency_lock_hash():
    if os.path.exists("requirements.txt"):
        return sha256_of_file("requirements.txt")
    return "no-requirements-file"


def get_node_version():
    try:
        return subprocess.check_output(["node", "--version"]).decode().strip()
    except Exception:
        return "node-not-installed"


def get_os_hash():
    uname = platform.uname()
    raw = f"{uname.system}-{uname.release}-{uname.version}-{uname.machine}"
    return hashlib.sha256(raw.encode()).hexdigest()


def generate_environment_fingerprint():
    env = {
        "python_version": sys.version,
        "node_version": get_node_version(),
        "platform": platform.platform(),
        "os_hash": get_os_hash(),
        "dependency_lock_hash": get_dependency_lock_hash()
    }

    with open("environment.json", "w") as f:
        json.dump(env, f, indent=2)

    combined = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()

    with open("environment.hash.txt", "w") as f:
        f.write(combined)

    return combined
