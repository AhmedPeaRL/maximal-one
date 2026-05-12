import hashlib
import json
from pathlib import Path

ARTIFACT = Path("artifacts/canonical_report.json")
STAMP_OUT = Path("artifacts/reproducibility_stamp.json")


def generate_stamp(path):

    content = path.read_bytes()

    return hashlib.sha256(content).hexdigest()


def attach_stamp():

    if not ARTIFACT.exists():
        raise SystemExit("❌ canonical_report.json missing")

    stamp = generate_stamp(ARTIFACT)

    payload = {
        "artifact": ARTIFACT.name,
        "sha256": stamp,
        "sealed": True
    }

    STAMP_OUT.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8"
    )

    print(json.dumps(payload, indent=2))
    print("✅ REPRODUCIBILITY STAMP SEALED")

    return stamp


if __name__ == "__main__":
    attach_stamp()
