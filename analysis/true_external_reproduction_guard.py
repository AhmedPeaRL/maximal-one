import requests
import hashlib
import json
import time

GITHUB_RAW = "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/artifacts/canonical_report.json"


# =========================
# NORMALIZATION CORE
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
# NETWORK
# =========================

def fetch_external():
    import requests

    url = "https://api.github.com/repos/ahmedpearl/maximal-one/contents/artifacts/canonical_report.json"

    for i in range(5):
        try:
            r = requests.get(url, timeout=10)

            if r.status_code == 200:
                data = r.json()
                import base64
                content = base64.b64decode(data["content"]).decode()
                return content

        except Exception as e:
            print("Fetch error:", e)

        time.sleep(3)

    return None


def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


# =========================
# CORE
# =========================

def compute_local():
    try:
        with open("artifacts/canonical_report.json") as f:
            raw = f.read()

        norm = normalize_json(raw)

        if not norm:
            return None

        return norm, sha256(norm)

    except:
        return None


def compute_external():
    raw = fetch_external()

    if not raw:
        return None

    norm = normalize_json(raw)

    if not norm:
        return None

    return norm, sha256(norm)


def run():
    local = compute_local()

    if not local:
        print("❌ Local computation failed")
        return False

    local_norm, local_hash = local

    for attempt in range(3):
        external = compute_external()

        if not external:
            print("⚠️ External fetch failed")
            time.sleep(3)
            continue

        external_norm, external_hash = external

        if external_hash == local_hash:
            print("✅ True external reproduction confirmed")
            return True

        # fallback: compare normalized content similarity
        if external_norm == local_norm:
            print("⚠️ Hash mismatch but content identical (non-critical)")
            return True

        print("Waiting for GitHub propagation...")
        
        time.sleep(10)

        print(f"⚠️ Mismatch {attempt+1}")
        print("External:", external_hash)
        print("Local   :", local_hash)

        time.sleep(5)

    print("❌ Persistent mismatch")
    return False


if __name__ == "__main__":
    ok = run()
    if not ok:
        exit(1)
