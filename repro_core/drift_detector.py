import json
import sys


def detect_drift(old_hash, new_hash):
    if old_hash != new_hash:
        return "DRIFT_DETECTED"
    return "NO_DRIFT"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: drift_detector.py <old> <new>")
        sys.exit(1)

    result = detect_drift(sys.argv[1], sys.argv[2])
    print(result)

    if result == "DRIFT_DETECTED":
        sys.exit(2)
