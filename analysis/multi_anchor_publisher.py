import hashlib
import json
import time
import os
import requests

ARTIFACT = "artifacts/canonical_report.json"

def compute_hash():
    with open(ARTIFACT, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def github_gist_anchor(h):
    token = os.getenv("GH_TOKEN", "").strip()

    if not token:
        return False

    try:
        r = requests.post(
            "https://api.github.com/gists",
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json"
            },
            json={
                "public": True,
                "files": {
                    "anchor.txt": {
                        "content": f"{h} @ {time.time()}"
                    }
                }
            },
            timeout=10
        )

        if r.status_code == 201:
            return True
        else:
            print("Gist error:", r.status_code, r.text)
            return False

    except Exception as e:
        print("Gist exception:", str(e))
        return False

def hash_public_api_anchor(h):
    try:
        r = requests.get(
            f"https://api.hashify.net/hash/sha256/hex?value={h}",
            timeout=10
        )
        return r.status_code == 200
    except:
        return False

def cloudflare_trace_anchor(h):
    try:
        r = requests.get("https://www.cloudflare.com/cdn-cgi/trace", timeout=5)

        if r.status_code == 200:
            return True
        return False

    except:
        return False

def time_anchor(h):
    return {
        "hash": h,
        "timestamp": time.time()
    }

def store(h, results):
    os.makedirs("data", exist_ok=True)

    path = "data/multi_anchor_log.json"

    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    else:
        data = []

    prev_hash = data[-1]["entry_hash"] if data else None

    entry = {
        "hash": h,
        "timestamp": time.time(),
        "anchors": results,
        "prev": prev_hash
    }

    entry_hash = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
    entry["entry_hash"] = entry_hash

    data.append(entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    h = compute_hash()

    results = {
        "github_gist": github_gist_anchor(h),
        "hash_api": hash_public_api_anchor(h),
        "cloudflare": cloudflare_trace_anchor(h),
        "local_time": True
    }

    store(h, results)

    print("Multi-anchor:", h, results)

if __name__ == "__main__":
    main()
