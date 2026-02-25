import subprocess
import json
import sys
from stability_metric import is_stable

result = subprocess.check_output(["python", "repro-core/deterministic_kernel.py"])
data = json.loads(result)

variance = data["state"]["variance"]

if not is_stable(variance):
    print("FAILURE_MODE: UNSTABLE_VARIANCE")
    sys.exit(1)

print("STABLE_UNDER_DEFINED_DOMAIN")
