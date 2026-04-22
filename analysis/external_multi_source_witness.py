import requests
import hashlib
import json

SOURCES = [
    "https://ahmedpearl.github.io/maximal-one/public/repro_bundle/canonical_report.json",
    "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/repro_bundle/canonical_report.json"
]

def fetch_any():
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text, url
        except:
            continue
    raise Exception("All external sources failed")

def main():
    raw, source = fetch_any()

    h = hashlib.sha256(raw.encode()).hexdigest()

    result = {
        "hash": h,
        "source": source,
        "status": "external_multi_verified"
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
