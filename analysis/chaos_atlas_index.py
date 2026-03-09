import json
import os
from datetime import datetime

DATA_DIR = "real-data"
OUTPUT = "artifacts/chaos_atlas_index.json"

def scan_datasets():
    atlas = []

    if not os.path.exists(DATA_DIR):
        return atlas

    for f in os.listdir(DATA_DIR):
        if not f.endswith(".csv"):
            continue

        path = os.path.join(DATA_DIR, f)

        entry = {
            "dataset": f,
            "path": path,
            "size_bytes": os.path.getsize(path),
            "timestamp": datetime.utcnow().isoformat()
        }

        atlas.append(entry)

    return atlas


def main():
    atlas = scan_datasets()

    os.makedirs("artifacts", exist_ok=True)

    with open(OUTPUT, "w") as f:
        json.dump(
            {
                "atlas_size": len(atlas),
                "datasets": atlas
            },
            f,
            indent=2
        )

    print(json.dumps({"atlas_size": len(atlas)}, indent=2))


if __name__ == "__main__":
    main()
