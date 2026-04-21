import requests
import hashlib
import os
import json
import time

GITHUB_RAW = f"https://raw.githubusercontent.com/ahmedpearl/maximal-one/{os.getenv('GITHUB_SHA')}/artifacts/canonical_report.json"

def normalize_json(raw_text):
    try:
        data = json.loads(raw_text)

        data.pop("_environment", None)
        data.pop("timestamp", None)

        # 🔥 تثبيت الفلوت
        def normalize_numbers(obj):
            if isinstance(obj, dict):
                return {k: normalize_numbers(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [normalize_numbers(x) for x in obj]
            elif isinstance(obj, float):
                return round(obj, 10)
            return obj

        data = normalize_numbers(data)

        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    except Exception:
        return None


def fetch_external(retries=3):
    for i in range(retries):
        try:
            r = requests.get(GITHUB_RAW, timeout=10)

            if r.status_code == 200:
                return r.text

        except:
            pass

        time.sleep(2)

    return None


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


def run():
    external_raw = fetch_external()

    if not external_raw:
        print("❌ External fetch failed")
        return False

    external_norm = normalize_json(external_raw)

    if not external_norm:
        print("❌ External normalization failed")
        return False

    external_hash = sha256(external_norm)

    with open("artifacts/canonical_report.json") as f:
        local_raw = f.read()

    local_norm = normalize_json(local_raw)

    if not local_norm:
        print("❌ Local normalization failed")
        return False

    local_hash = sha256(local_norm)

    if external_hash != local_hash:
        print("❌ External mismatch (normalized)")
        print("External:", external_hash)
        print("Local   :", local_hash)
        return False

    print("✅ True external reproduction confirmed (normalized)")
    return True


if __name__ == "__main__":
    ok = run()
    if not ok:
        exit(1)
