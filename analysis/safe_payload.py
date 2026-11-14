"""Safe JSON payload boundary for GitHub Actions.

Untrusted GitHub event data is read from an environment variable and parsed as
JSON. It is never interpolated into shell source or evaluated as a command.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


def normalize_payload(raw: str | None) -> Any:
    if raw is None or raw == "" or raw == "null":
        return {"_empty": True}

    data = json.loads(raw)

    if data is None:
        raise ValueError("Null payload rejected")

    # Preserve the existing 5,000-character guard from the workflow.
    serialized = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if len(serialized) > 5000:
        raise ValueError("Payload too large")

    if isinstance(data, dict) and data == {}:
        raise ValueError("Empty object payload rejected")

    return data


def write_payload(raw: str | None, output: Path, checksum: Path | None = None) -> Any:
    data = normalize_payload(raw)
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
    output.write_text(serialized, encoding="utf-8")
    if checksum is not None:
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        checksum.parent.mkdir(parents=True, exist_ok=True)
        checksum.write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--sha256", default=None)
    args = parser.parse_args()

    raw = os.environ.get("CLIENT_PAYLOAD_JSON", "null")
    write_payload(
        raw,
        Path(args.output),
        Path(args.sha256) if args.sha256 else None,
    )
    print("Payload parsed and staged as data; no shell evaluation performed.")


if __name__ == "__main__":
    main()
