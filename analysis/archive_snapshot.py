import shutil
import hashlib
from pathlib import Path

SOURCE = Path("artifacts/canonical_report.json")

content = SOURCE.read_bytes()

digest = hashlib.sha256(
    content
).hexdigest()[:16]

dest_dir = Path("artifacts/archive")

dest_dir.mkdir(
    parents=True,
    exist_ok=True
)

dest = dest_dir / f"{digest}.json"

if not dest.exists():

    shutil.copy2(
        SOURCE,
        dest
    )

    print(
        f"✅ Snapshot archived: {dest}"
    )

else:

    print(
        f"ℹ️ Snapshot already exists: {dest}"
    )
