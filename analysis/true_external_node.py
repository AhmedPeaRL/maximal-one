import requests
import hashlib
import json
import time


URL = "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/artifacts/canonical_report.json"


def fetch():
    for i in range(5):
        try:
            r = requests.get(URL + f"?t={int(time.time())}", timeout=15)

            if r.status_code == 200:
                return r.text

        except Exception as e:
            print("Fetch error:", e)

        time.sleep(3)

    raise Exception("Failed to fetch external canonical report")


def normalize(raw):
    try:
        data = json.loads(raw)

        VOLATILE_KEYS = {
            "timestamp",
            "_environment",
            "generated_at",
            "runtime",
            "execution_time",
            "host",
            "_sealed"
        }

        def strip(obj):
            if isinstance(obj, dict):
                return {
                    k: strip(v)
                    for k, v in obj.items()
                    if k not in VOLATILE_KEYS
                }
            elif isinstance(obj, list):
                return [strip(x) for x in obj]
            elif isinstance(obj, float):
                return round(obj, 8)
            return obj

        clean = strip(data)

        return json.dumps(clean, sort_keys=True, separators=(',', ':'))

    except Exception:
        return None


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


def main():
    print("=== TRUE EXTERNAL NODE ===")

    raw = fetch()

    norm = normalize(raw)

    if not norm:
        raise Exception("Normalization failed")

    h = sha256(norm)

    print("External hash:", h)

    with open("external_result.json", "w") as f:
        json.dump({
            "timestamp": time.time(),
            "external_hash": h,
            "source": "independent_node",
            "normalized": True
        }, f, indent=2)


if __name__ == "__main__":
    main()
