import requests, hashlib, json

URL = "https://ahmedpearl.github.io/maximal-one/public/repro_bundle/canonical_report.json"
HASH_URL = "https://ahmedpearl.github.io/maximal-one/public/repro_bundle/report.hash"

r = requests.get(URL)
data = r.text

h = hashlib.sha256(data.encode()).hexdigest()

expected = requests.get(HASH_URL).text.strip()

print("Computed:", h)
print("Expected:", expected)

if h == expected:
    print("MATCH ✅")
else:
    print("MISMATCH ❌")
