import json
import os
import time
import hashlib
import requests

BREACH_LOG = "data/reality_breach_log.json"

PUBLIC_ENDPOINTS = [
    "https://api.coindesk.com/v1/bpi/currentprice.json",
    "https://worldtimeapi.org/api/timezone/Etc/UTC",
    "https://api.github.com"
]

def fetch_external_signal():
    results = []

    for url in PUBLIC_ENDPOINTS:
        try:
            r = requests.get(url, timeout=5)
            results.append({
                "url": url,
                "status": r.status_code,
                "hash": hashlib.sha256(r.text.encode()).hexdigest()
            })
        except Exception as e:
            results.append({
                "url": url,
                "error": str(e)
            })

    return results


def evaluate_breach(signals):
    score = 0

    for s in signals:
        if "status" in s and s["status"] == 200:
            score += 1

    return {
        "breach_score": score,
        "total_sources": len(signals),
        "status": "stable" if score >= 2 else "unstable"
    }


def persist(log):
    os.makedirs("data", exist_ok=True)

    if os.path.exists(BREACH_LOG):
        with open(BREACH_LOG, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log)

    with open(BREACH_LOG, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    signals = fetch_external_signal()
    evaluation = evaluate_breach(signals)

    record = {
        "timestamp": int(time.time()),
        "signals": signals,
        "evaluation": evaluation
    }

    persist(record)

    print("Reality breach evaluated:", evaluation)
