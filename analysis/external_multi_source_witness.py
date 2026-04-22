import requests
import hashlib
import json

SOURCES = [
    "https://ahmedpearl.github.io/maximal-one/public/repro_bundle/canonical_report.json",
    "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/repro_bundle/canonical_report.json",
    "https://cdn.jsdelivr.net/gh/ahmedpearl/maximal-one@main/public/repro_bundle/canonical_report.json",
    "https://raw.githack.com/ahmedpearl/maximal-one/main/public/repro_bundle/canonical_report.json"
]

def fetch_any():
    errors = []

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and len(r.text.strip()) > 0:
                return r.text, url
            else:
                errors.append(f"{url} -> bad response")
        except Exception as e:
            errors.append(f"{url} -> {str(e)}")

    return None, errors

def main():
    raw, meta = fetch_any()

    if raw is None:
        result = {
            "status": "degraded",
            "errors": meta
        }
        print(json.dumps(result, indent=2))
        return

    h = hashlib.sha256(raw.encode()).hexdigest()

    result = {
        "hash": h,
        "source": meta,
        "status": "external_multi_verified"
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
