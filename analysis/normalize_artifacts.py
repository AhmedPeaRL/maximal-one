import json
from pathlib import Path

ARTIFACTS = Path("artifacts")

for path in sorted(ARTIFACTS.glob("*.json")):

    try:
        data = json.loads(path.read_text())

        path.write_text(
            json.dumps(
                data,
                indent=2,
                sort_keys=True
            ) + "\n"
        )

    except Exception:
        pass

print("✅ ARTIFACT NORMALIZATION COMPLETE")
