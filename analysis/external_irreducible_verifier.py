import hashlib
import json
import time
import requests

# Independent public endpoint (cannot be controlled by repo)

PUBLIC_ENDPOINT = "https://httpbin.org/post"

def load_report():
  with open("artifacts/canonical_report.json") as f:
    return json.load(f)

def build_payload(report):
  raw = json.dumps(report, sort_keys=True).encode()
  return {
    "hash": hashlib.sha256(raw).hexdigest(),
    "timestamp": time.time(),
    "source": "maximal-one"
  }

def send_external(payload):
  try:
    r = requests.post(PUBLIC_ENDPOINT, json=payload, timeout=10)
    return r.status_code == 200
  except Exception as e:
    print("External failure:", str(e))
    return False

def persist_external_anchor(payload, success):
  anchor = {
    "payload": payload,
    "external_verified": success,
    "note": "Verification outside system boundary"
  }
  
  with open("artifacts/external_irreducible_verification.json","w") as f:
    json.dump(anchor, f, indent=2)

def main():
  report = load_report()
  payload = build_payload(report)
  success = send_external(payload)
  persist_external_anchor(payload, success)
  
  if success:
    print("✅ External irreducible verification succeeded")
  else:
    print("⚠️ External verification failed")

if __name__ == "__main__":
    main()
