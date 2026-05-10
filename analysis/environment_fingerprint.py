import hashlib
import json
import platform
import sys

from importlib.metadata import distributions

packages = sorted([
    f"{d.metadata['Name']}=={d.version}"
    for d in distributions()
])

env = {
    "python": sys.version,
    "platform": platform.platform(),
    "packages": packages
}

serialized = json.dumps(
    env,
    sort_keys=True
).encode()

fp = hashlib.sha256(
    serialized
).hexdigest()

result = {
    "environment_fingerprint": fp,
    "package_count": len(packages)
}

with open(
    "artifacts/environment_fingerprint.json",
    "w"
) as f:
    json.dump(result, f, indent=2)

print(json.dumps(
    result,
    indent=2
))

print(
    "✅ ENVIRONMENT FINGERPRINT SEALED"
)
