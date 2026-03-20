import json
import os
from datetime import datetime

HISTORY = "data/invariant_history.json"


def safe_load_json(path):
    if not os.path.exists(path):
        return []

    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Corrupted history detected: {e}")

        # 🧠 fallback: rename corrupted file
        corrupted_path = path + ".corrupted"
        os.rename(path, corrupted_path)

        print(f"[RECOVERY] Corrupted file moved to {corrupted_path}")

        return []


def safe_write_json(path, data):
    tmp_path = path + ".tmp"

    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)

    os.replace(tmp_path, path)


def main():
    hist = safe_load_json(HISTORY)

    try:
        with open("artifacts/invariants.json") as f:
            new = json.load(f)
    except Exception as e:
        print(f"[ERROR] Cannot load new invariants: {e}")
        return

    entry = {
        "time": datetime.utcnow().isoformat(),
        "results": new
    }

    hist.append(entry)

    os.makedirs("data", exist_ok=True)

    safe_write_json(HISTORY, hist)


if __name__ == "__main__":
    main()
