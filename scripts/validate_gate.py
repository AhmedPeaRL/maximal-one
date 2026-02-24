# scripts/validate_gate.py

import json
import sys
import hashlib
import platform
import subprocess


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def environment_fingerprint():
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_gate.py <report.json>")
        sys.exit(1)

    report_path = sys.argv[1]

    with open(report_path, "r") as f:
        report = json.load(f)

    required_keys = ["mean", "std", "p95", "p99"]

    for k in required_keys:
        if k not in report:
            print(f"Missing key in report: {k}")
            sys.exit(1)

    if report["p99"] > 6.0:
        print("Stability breach: p99 exceeds threshold")
        sys.exit(1)

    digest = sha256_of_file(report_path)

    print("Report SHA256:", digest)
    print("Environment:", environment_fingerprint())
    print("Gate validation passed.")


if __name__ == "__main__":
    main()
