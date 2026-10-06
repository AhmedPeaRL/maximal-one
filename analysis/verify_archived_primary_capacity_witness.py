#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path


ARTIFACT = Path(
    "artifacts/primary_null_capacity_audit.json"
)

REQUIRED_KEYS = [
    "seed",
    "valid_surrogate_refits",
    "valid_surrogate_alpha_estimates",
]


def fail(message):
    raise SystemExit(f"❌ {message}")


def main():
    if not ARTIFACT.is_file():
        fail(
            "Raw primary capacity audit artifact is missing."
        )

    raw = ARTIFACT.read_bytes()

    if not raw:
        fail(
            "Primary capacity audit artifact is empty."
        )

    try:
        data = json.loads(
            raw.decode("utf-8")
        )
    except Exception as exc:
        fail(
            f"Artifact is not valid JSON: {exc}"
        )

    for key in REQUIRED_KEYS:
        if key not in data:
            fail(
                f"Required witness field missing: {key}"
            )

    valid_refits = int(
        data["valid_surrogate_refits"]
    )

    valid_alpha = int(
        data["valid_surrogate_alpha_estimates"]
    )

    if valid_refits != 1000:
        fail(
            "Archived witness does not record "
            "the declared 1000 valid surrogate refits."
        )

    if valid_alpha != 1000:
        fail(
            "Archived witness does not record "
            "1000 valid alpha estimates."
        )

    digest = hashlib.sha256(
        raw
    ).hexdigest()

    print(
        "✅ Raw primary capacity witness verified."
    )
    print(
        f"SHA256: {digest}"
    )
    print(
        "Scientific role: diagnostic_only"
    )
    print(
        "Claim promotion: blocked"
    )


if __name__ == "__main__":
    main()
