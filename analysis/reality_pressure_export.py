import json
import time
import hashlib
import os
import requests

EXPORT_ENDPOINT = os.getenv("RPEL_ENDPOINT", "https://httpbin.org/post")

def load_signal():
    try:
        with open("public/live_truth.json") as f:
            return json.load(f)
    except:
        return None

def build_pressure_packet(signal):
    raw = json.dumps(signal, sort_keys=True)
    h = hashlib.sha256(raw.encode()).hexdigest()

    return {
        "timestamp": time.time(),
        "hash": h,
        "signal": signal,
        "intent": "external_pressure"
    }

def export_pressure(packet):
    try:
        r = requests.post(EXPORT_ENDPOINT, json=packet, timeout=10)
        return {
            "status": "sent",
            "code": r.status_code
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

def main():
    signal = load_signal()

    if not signal:
        print("No signal → skipping")
        return

    packet = build_pressure_packet(signal)
    result = export_pressure(packet)

    os.makedirs("data", exist_ok=True)

    with open(f"data/pressure_{int(time.time())}.json","w") as f:
        json.dump({
            "packet": packet,
            "result": result
        }, f, indent=2)

    print("Pressure export:", result)

if __name__ == "__main__":
    main()
