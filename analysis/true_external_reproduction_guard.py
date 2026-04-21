import requests
import hashlib
import json
import time

GITHUB_RAW = "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/artifacts/canonical_report.json"


# =========================
# NORMALIZATION CORE (HARDENED)
# =========================

VOLATILE_KEYS = {
    "timestamp",
    "_environment",
    "generated_at",
    "runtime",
    "execution_time",
    "host",
}


def strip_volatile(obj):
    if isinstance(obj, dict):
        return {
            k: strip_volatile(v)
            for k, v in obj.items()
            if k not in VOLATILE_KEYS
        }
    elif isinstance(obj, list):
        return [strip_volatile(x) for x in obj]
    return obj


def normalize_numbers(obj):
    if isinstance(obj, dict):
        return {k: normalize_numbers(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_numbers(x) for x in obj]
    elif isinstance(obj, float):
        return round(obj, 8)
    return obj


def normalize_json(raw_text):
    try:
        data = json.loads(raw_text)

        data = strip_volatile(data)
        data = normalize_numbers(data)

        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    except Exception:
        return None


# =========================
# NETWORK LAYER (STRONGER)
# =========================

def fetch_external():
    for i in range(6):  # 🔥 increased retries
        try:
            r = requests.get(GITHUB_RAW, timeout=15)

            if r.status_code == 200:
                return r.text

        except:
            pass

        time.sleep(3 * (i + 1))

    return None


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


# =========================
# CORE LOGIC
# =========================

def compute_local():
    with open("artifacts/canonical_report.json") as f:
        raw = f.read()

    norm = normalize_json(raw)

    if not norm:
        return None

    return sha256(norm)


def compute_external():
    raw = fetch_external()

    if not raw:
        return None

    norm = normalize_json(raw)

    if not norm:
        return None

    return sha256(norm)


def run():
    local_hash = compute_local()

    if not local_hash:
        print("❌ Local normalization failed")
        return False

    for attempt in range(3):
        external_hash = compute_external()

        if not external_hash:
            print("⚠️ External fetch failed, retrying...")
            time.sleep(5)
            continue

        if external_hash == local_hash:
            print("✅ True external reproduction confirmed")
            return True

        print(f"⚠️ Mismatch attempt {attempt+1}")
        print("External:", external_hash)
        print("Local   :", local_hash)

        time.sleep(8)

    print("❌ Persistent mismatch")
    return False


if __name__ == "__main__":
    ok = run()
    if not ok:
        exit(1)
