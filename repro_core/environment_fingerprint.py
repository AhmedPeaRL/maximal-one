import json
import hashlib
import platform
import sys
import subprocess


def get_env_fingerprint():
    env_data = {
        "python_version": sys.version,
        "python_build": platform.python_build(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "system": platform.system(),
        "release": platform.release(),
    }

    try:
        openssl = subprocess.check_output(
            ["openssl", "version"], text=True
        ).strip()
        env_data["openssl_version"] = openssl
    except Exception:
        env_data["openssl_version"] = "unavailable"

    canonical = json.dumps(env_data, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()

    return {
        "fingerprint": digest,
        "environment": env_data,
    }


if __name__ == "__main__":
    result = get_env_fingerprint()
    print(json.dumps(result, indent=2))
