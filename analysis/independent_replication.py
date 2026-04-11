import requests
import json
import time

ENDPOINT = "https://httpbin.org/post"


def trigger_replication(report_hash):
    payload = {
        "type": "independent_replication_request",
        "report_hash": report_hash,
        "timestamp": time.time()
    }

    try:
        r = requests.post(ENDPOINT, json=payload, timeout=5)

        result = {
            "status": r.status_code,
            "response": r.text[:200]
        }

    except Exception as e:
        result = {
            "status": 500,
            "error": str(e)
        }

    with open("artifacts/independent_replication.json", "w") as f:
        json.dump({
            "payload": payload,
            "result": result
        }, f, indent=2)

    print("Replication trigger sent.")


if __name__ == "__main__":
    trigger_replication("unknown")
