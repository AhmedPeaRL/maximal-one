import sys
import json
import hashlib


def canonicalize(obj):
    """
    Produce canonical JSON representation:
    - Sorted keys
    - No whitespace noise
    - Deterministic float formatting
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        print(f"Invalid JSON input: {e}")
        sys.exit(1)

    canonical = canonicalize(data)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    print(digest)


if __name__ == "__main__":
    main()
