import shutil
from pathlib import Path
from datetime import datetime

SOURCE = "artifacts/canonical_report.json"

timestamp = datetime.utcnow().strftime(
    "%Y%m%dT%H%M%SZ"
)

dest_dir = Path(
    "artifacts/archive"
)

dest_dir.mkdir(
    parents=True,
    exist_ok=True
)

dest = dest_dir / f"{timestamp}.json"

shutil.copy2(
    SOURCE,
    dest
)

print(
    f"✅ Snapshot archived: {dest}"
)
