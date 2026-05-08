import hashlib
import json
import pkg_resources
import platform
import sys

packages = sorted([
    f"{p.project_name}=={p.version}"
    for p in pkg_resources.working_set
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
