from __future__ import annotations

import json
from pathlib import Path


SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
}


def reject_constant(value: str):
    raise ValueError(
        f"non-standard JSON constant: {value}"
    )


def validate_json(path: Path) -> None:
    text = path.read_text(
        encoding="utf-8"
    )

    json.loads(
        text,
        parse_constant=reject_constant,
    )


def main() -> None:
    failures = []

    for path in Path(".").rglob("*.json"):

        if any(
            part in SKIP_DIRS
            for part in path.parts
        ):
            continue

        try:
            validate_json(path)

        except Exception as exc:
            failures.append(
                f"{path}: {exc}"
            )

    if failures:
        print(
            "❌ JSON integrity guard failed:"
        )

        for failure in failures:
            print(
                f" - {failure}"
            )

        raise SystemExit(1)

    print(
        "✅ JSON integrity guard passed."
    )


if __name__ == "__main__":
    main()
